from playwright.sync_api import sync_playwright
import csv
from scraper.config import *
from scraper.url_builder import build_url
from scraper.scraper import scrape_page
from scraper.navigator import navigate_to_next_page
from scraper.exporter import save_to_csv
from model.car import Car

def read_existing_cars(filename):
    """Read existing cars from CSV file."""
    cars = set()
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                car = Car(
                    title=row["Título"],
                    price=int(row["Precio"]),
                    year=int(row["Año"]),
                    km=int(row["Kilometraje"]),
                    link=row["Enlace"],
                    location=row["Ubicación"]
                )
                cars.add(car)
    except FileNotFoundError:
        print("📄 No se encontró archivo existente, se creará uno nuevo.")
    return cars

def main(append_mode=True):
    INITIAL_URL = build_url(SEARCH_OPTIONS)
    print(INITIAL_URL)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=REAL_USER_AGENT, locale="es-CO")
        page = context.new_page()

        # Get existing cars if in append mode
        existing_cars = read_existing_cars(CSV_LIST) if append_mode else set()
        print(f"\n📊 Modo: {'Añadir' if append_mode else 'Sobrescribir'}")
        if append_mode:
            print(f"📄 Carros existentes: {len(existing_cars)}")

        # Scrape new cars
        new_cars = set()  # Using a set to automatically handle duplicates
        page.goto(INITIAL_URL)
        current_page = 1

        while current_page <= MAX_PAGES:
            try:
                cars = scrape_page(page, current_page)
                new_cars.update(cars)

                if not navigate_to_next_page(page, MIN_WAIT_TIME, MAX_WAIT_TIME):
                    print("🚫 No hay más páginas.")
                    break

                current_page += 1

            except Exception as e:
                print(f"❌ Error en la página {current_page}: {e}")
                break

        # Combine cars based on mode
        if append_mode:
            # Add new cars to existing ones (duplicates will be automatically handled)
            all_cars = existing_cars.union(new_cars)
            print(f"🆕 Carros nuevos encontrados: {len(new_cars)}")
            print(f"📈 Carros duplicados ignorados: {len(existing_cars) + len(new_cars) - len(all_cars)}")
        else:
            all_cars = new_cars
            print(f"🆕 Carros encontrados: {len(new_cars)}")

        # Convert set to list for scoring
        cars_list = list(all_cars)
        save_to_csv(cars_list, CSV_LIST)
        print(f"\n✅ Datos guardados en {CSV_LIST} con {len(cars_list)} registros.")
        browser.close()

if __name__ == "__main__": main()
