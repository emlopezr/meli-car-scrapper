from model.car import Car

def normalize_number(text):
  """Convert text to number by removing non-digit characters."""
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
