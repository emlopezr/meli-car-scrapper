import sys
from list_cars.browser import setup_browser, close_browser
from list_cars.scraper import scrape_cars
from list_cars.data import load_existing_cars, process_results, save_results
from list_cars.url_builder import build_url
from utils.config import get_scraping_config

def main(append_mode=True):
  """Main function to scrape and save car listings."""
  config = get_scraping_config()
  initial_url = build_url(config['search_options'])
  output_file = sys.argv[1]

  playwright, browser, page = setup_browser()

  try:
    existing_cars = load_existing_cars(output_file, append_mode)
    new_cars = scrape_cars(page, initial_url)
    cars_list = process_results(existing_cars, new_cars, append_mode)
    save_results(cars_list, output_file)
  finally:
    close_browser(playwright, browser)

if __name__ == "__main__":
  main()
