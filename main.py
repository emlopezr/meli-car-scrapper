from playwright.sync_api import sync_playwright
import time
import random
import csv
from model.car import Car

REAL_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.6367.61 Safari/537.36"
)

OPTIONS = {
    "gear": "automatica",
    "type": "camioneta",
    "location": "antioquia",
    "min_year": 2012,
    "max_price": 65000000,
    "has_abs_brakes": True,
    "has_air_conditioning": True,
    "has_power_windows": True,
}

BASE_URL = "https://carros.mercadolibre.com.co"

def build_url(options):
    filters = []
    filters.append(options['gear'])
    
    if options.get('has_abs_brakes', False): filters.append('con-frenos-abs')
    if options.get('has_air_conditioning', False): filters.append('con-aire-acondicionado')
    if options.get('has_power_windows', False): filters.append('con-vidrios-electricos')
    
    filters.extend([options['type'], options['location']])
    
    url = f"{BASE_URL}/{'/'.join(filters)}/desde-{options['min_year']}/"
    url += f"_PriceRange_0-{options['max_price']}"
    url += "_NoIndex_True" 
    
    return url

def normalize_number(text):
    return int(''.join(c for c in text if c.isdigit())) if text else 0

def extract_car_data(item):
    """Extract data from a single car listing item."""
    try:
        title_el = item.query_selector("a.poly-component__title")
        price_el = item.query_selector("span.andes-money-amount__fraction")
        attrs = item.query_selector_all("ul.poly-attributes-list li")
        location_el = item.query_selector("span.poly-component__location")

        title = title_el.inner_text().strip() if title_el else ""
        link = title_el.get_attribute("href") if title_el else ""
        price = normalize_number(price_el.inner_text()) if price_el else 0
        year = int(attrs[0].inner_text().strip()) if len(attrs) > 0 else 0
        km = normalize_number(attrs[1].inner_text()) if len(attrs) > 1 else 0
        location = location_el.inner_text().strip() if location_el else ""

        return Car(title, price, year, km, link, location)
    except Exception as e:
        print(f"⚠️ Error procesando item: {e}")
        return None

def scrape_page(page, page_number):
    """Scrape all car listings from a single page."""
    results = []
    page.wait_for_selector("ol.ui-search-layout.ui-search-layout--grid")
    items = page.query_selector_all("li.ui-search-layout__item")

    print(f"\n📄 Página {page_number} - 🚗 {len(items)} encontrados")
    
    for item in items:
        car = extract_car_data(item)
        if car:
            results.append(car)
            print(f"• {car.title} - {car.year} - {car.km} - {car.price}")

    return results

def compute_scores(cars):
    """Calculate scores for each car based on price, year, and kilometers."""
    prices = [car.price for car in cars if car.price > 0]
    years = [car.year for car in cars if car.year > 0]
    kms = [car.km for car in cars if car.km > 0]

    min_price, max_price = min(prices), max(prices)
    min_year, max_year = min(years), max(years)
    min_km, max_km = min(kms), max(kms)

    for car in cars:
        norm_price = (car.price - min_price) / (max_price - min_price) if max_price != min_price else 0
        norm_year = (car.year - min_year) / (max_year - min_year) if max_year != min_year else 0
        norm_km = (car.km - min_km) / (max_km - min_km) if max_km != min_km else 0

        score = (norm_year * 0.4 + (1 - norm_km) * 0.3 + (1 - norm_price) * 0.3) * 100
        car.score = round(score, 1)

    return cars

def save_to_csv(cars, filename):
    """Save the car data to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Título", "Precio", "Año", "Kilometraje", "Ubicación", "Enlace", "Score"])
        for car in cars:
            writer.writerow([
                car.title,
                car.price,
                car.year,
                car.km,
                car.location,
                car.link,
                car.score
            ])

def scroll_to_bottom(page):
    """Scroll to the bottom of the page smoothly."""
    page.evaluate("""
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
    """)
    # Wait a bit for the scroll to complete
    time.sleep(1)

def has_next_page(page):
    """Check if there is a next page available."""
    scroll_to_bottom(page)
    next_button = page.query_selector('li.andes-pagination__button--next:not(.andes-pagination__button--disabled)')
    return next_button is not None

def navigate_to_next_page(page, min_wait, max_wait):
    """Navigate to the next page if available."""
    try:
        # Check if next button exists and is not disabled
        if not has_next_page(page):
            return False

        # Wait for the next button to be visible and clickable
        next_button = page.wait_for_selector(
            'li.andes-pagination__button--next:not(.andes-pagination__button--disabled)', 
            state="visible", 
            timeout=10000
        )
        
        if next_button:
            wait_time = random.randint(min_wait, max_wait)
            print(f"⏸️ Esperando {wait_time} segundos antes de pasar de página...")
            time.sleep(wait_time)

            # Try to click with force if normal click fails
            try:
                next_button.click()
            except:
                page.evaluate('document.querySelector(\'li.andes-pagination__button--next:not(.andes-pagination__button--disabled)\').click()')
            
            # Wait for navigation to complete
            page.wait_for_load_state("networkidle")
            return True
    except Exception as e:
        print(f"⚠️ Error al navegar a la siguiente página: {e}")
    return False

def main():
    MAX_PAGES = 7  # Maximum number of pages to scrape
    MIN_WAIT_TIME = 20
    MAX_WAIT_TIME = 40
    OUTPUT_FILE = "carros.csv"
    INITIAL_URL = build_url(OPTIONS)
    
    print(INITIAL_URL)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=REAL_USER_AGENT, locale="es-CO")
        page = context.new_page()

        all_cars = set()  # Using a set to automatically handle duplicates
        page.goto(INITIAL_URL)
        current_page = 1

        while current_page <= MAX_PAGES:
            try:
                cars = scrape_page(page, current_page)

                # Add new cars to the set (duplicates will be automatically handled)
                all_cars.update(cars)

                if not navigate_to_next_page(page, MIN_WAIT_TIME, MAX_WAIT_TIME):
                    print("🚫 No hay más páginas.")
                    break

                current_page += 1

            except Exception as e:
                print(f"❌ Error en la página {current_page}: {e}")
                break

        # Convert set to list for scoring
        cars_list = list(all_cars)
        cars_with_scores = compute_scores(cars_list)
        save_to_csv(cars_with_scores, OUTPUT_FILE)
        print(f"\n✅ Datos guardados en {OUTPUT_FILE} con {len(cars_with_scores)} registros.")
        browser.close()

if __name__ == "__main__":
    main()
