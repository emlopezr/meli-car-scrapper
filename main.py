from playwright.sync_api import sync_playwright
from scraper.config import *
from scraper.url_builder import build_url
from scraper.scraper import scrape_page, compute_scores
from scraper.navigator import navigate_to_next_page
from scraper.exporter import save_to_csv

def main():
  INITIAL_URL = build_url(DEFAULT_OPTIONS)

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

if __name__ == "__main__": main()
