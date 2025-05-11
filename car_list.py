from playwright.sync_api import sync_playwright
import csv
import sys
from scraper.config import *
from scraper.url_builder import build_url
from scraper.scraper import scrape_page
from scraper.navigator import navigate_to_next_page
from scraper.exporter import save_to_csv, read_existing_cars

def setup_browser():
  """Initialize and return browser context."""
  playwright = sync_playwright().start()
  browser = playwright.chromium.launch(headless=False)
  context = browser.new_context(user_agent=USER_AGENT, locale="es-CO")
  page = context.new_page()

  return playwright, browser, page

def load_existing_cars(output_file, append_mode):
  """Load existing cars if in append mode."""
  existing_cars = read_existing_cars(output_file) if append_mode else set()

  print(f"\n📊 Modo: {'Añadir' if append_mode else 'Sobrescribir'}")
  if append_mode: print(f"📄 Carros existentes: {len(existing_cars)}")

  return existing_cars

def scrape_cars(page, initial_url):
  """Scrape cars from all available pages."""
  new_cars = set()
  current_page = 1
  
  page.goto(initial_url)

  while current_page <= MAX_SCRAPE_PAGES:
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

  return new_cars

def process_results(existing_cars, new_cars, append_mode):
  """Process and combine results based on mode."""
  if append_mode:
    all_cars = existing_cars.union(new_cars)
    print(f"🆕 Carros nuevos encontrados: {len(new_cars)}")
    print(f"📈 Carros duplicados ignorados: {len(existing_cars) + len(new_cars) - len(all_cars)}")

  else:
    all_cars = new_cars
    print(f"🆕 Carros encontrados: {len(new_cars)}")
  
  return list(all_cars)

def main(append_mode = True):
  """Main function to scrape and save car listings."""
  initial_url = build_url(SEARCH_OPTIONS)
  output_file = sys.argv[1]

  playwright, browser, page = setup_browser()
  
  try:
    existing_cars = load_existing_cars(output_file, append_mode)
    new_cars = scrape_cars(page, initial_url)
    cars_list = process_results(existing_cars, new_cars, append_mode)
    save_to_csv(cars_list, output_file)

    print(f"\n✅ Datos guardados en {output_file} con {len(cars_list)} registros.")

  finally:
    browser.close()
    playwright.stop()

if __name__ == "__main__": main()
