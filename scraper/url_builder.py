from .config import *

URL_FILTER_ABS_BRAKES = "con-frenos-abs"
URL_FILTER_AIR_CONDITIONING = "con-aire-acondicionado"
URL_FILTER_POWER_WINDOWS = "con-vidrios-electricos"
URL_FILTER_YEAR_PREFIX = "desde-"
URL_FILTER_PRICE_RANGE = "_PriceRange_0-"
URL_FILTER_NO_INDEX = "_NoIndex_True"

def build_url(options):
  """Build the search URL based on the provided options."""
  filters = []
  
  if options.get(OPTION_GEAR, False): 
    filters.append(options[OPTION_GEAR])
  
  if options.get(OPTION_HAS_ABS_BRAKES, False): 
    filters.append(URL_FILTER_ABS_BRAKES)
  
  if options.get(OPTION_HAS_AIR_CONDITIONING, False): 
    filters.append(URL_FILTER_AIR_CONDITIONING)
  
  if options.get(OPTION_HAS_POWER_WINDOWS, False): 
    filters.append(URL_FILTER_POWER_WINDOWS)
  
  if options.get(OPTION_TYPE, False): 
    filters.append(options[OPTION_TYPE])
  
  if options.get(OPTION_LOCATION, False): 
    filters.append(options[OPTION_LOCATION])
  
  url = f"{BASE_URL}/{'/'.join(filters)}/"
  url += f"{URL_FILTER_YEAR_PREFIX}{options[OPTION_MIN_YEAR]}/" 
  url += f"{URL_FILTER_PRICE_RANGE}{options[OPTION_MAX_PRICE]}"
  url += URL_FILTER_NO_INDEX
  
  return url
