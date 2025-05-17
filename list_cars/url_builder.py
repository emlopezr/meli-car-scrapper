from utils.config import get_scraping_config

URL_FILTER_ABS_BRAKES = "con-frenos-abs"
URL_FILTER_AIR_CONDITIONING = "con-aire-acondicionado"
URL_FILTER_POWER_WINDOWS = "con-vidrios-electricos"
URL_FILTER_YEAR_PREFIX = "desde-"
URL_FILTER_PRICE_RANGE = "_PriceRange_0-"
URL_FILTER_NO_INDEX = "_NoIndex_True"

def build_url(options):
  """Build the search URL based on the provided options."""
  config = get_scraping_config()
  base_url = config['base_url']
  filters = []

  if options.get("gear", False):
    filters.append(options["gear"])

  if options.get("model", False):
    filters.append(options["model"])

  if options.get("has_abs_brakes", False):
    filters.append(URL_FILTER_ABS_BRAKES)

  if options.get("has_air_conditioning", False):
    filters.append(URL_FILTER_AIR_CONDITIONING)

  if options.get("has_power_windows", False):
    filters.append(URL_FILTER_POWER_WINDOWS)

  if options.get("type", False):
    filters.append(options["type"])

  if options.get("location", False): 
    filters.append(options["location"])

  url = f"{base_url}/{'/'.join(filters)}/"
  url += f"{URL_FILTER_YEAR_PREFIX}{options['min_year']}/" 
  url += f"{URL_FILTER_PRICE_RANGE}{options['max_price']}"
  url += URL_FILTER_NO_INDEX

  return url
