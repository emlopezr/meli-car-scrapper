from models.car import Car
from .config import get_scraping_config
from .navigator import navigate_to_next_page

def extract_car_data(item):
  """Extract data from a single car listing item."""
  try:
    title_el = item.query_selector("a.poly-component__title")
    price_el = item.query_selector("span.andes-money-amount__fraction")

    title = title_el.inner_text().strip() if title_el else ""
    price = price_el.inner_text().strip() if price_el else "0"
    link = title_el.get_attribute("href") if title_el else ""

    return Car(title, price, link)
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
      print(f"• {car.title} - ${car.price}")

  return results

def scrape_cars(page, initial_url):
  """Scrape cars from all available pages."""
  config = get_scraping_config()
  new_cars = set()
  current_page = 1

  page.goto(initial_url)

  while current_page <= config['max_pages']:
    try:
      cars = scrape_page(page, current_page)
      new_cars.update(cars)

      if not navigate_to_next_page(page):
        print("🚫 No hay más páginas.")
        break

      current_page += 1

    except Exception as e:
      print(f"\n❌ Error en la página {current_page}: {e}")
      break

  return new_cars 