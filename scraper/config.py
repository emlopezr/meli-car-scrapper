import sys

BASE_URL = "https://carros.mercadolibre.com.co"

USER_AGENT = (
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
  "Chrome/124.0.6367.61 Safari/537.36"
)

# Search options
OPTION_LOCATION = "location"
OPTION_GEAR = "gear"
OPTION_TYPE = "type"
OPTION_MIN_YEAR = "min_year"
OPTION_MAX_PRICE = "max_price"
OPTION_HAS_ABS_BRAKES = "has_abs_brakes"
OPTION_HAS_AIR_CONDITIONING = "has_air_conditioning"
OPTION_HAS_POWER_WINDOWS = "has_power_windows"

SEARCH_OPTIONS = {
  OPTION_GEAR: "automatica",
  OPTION_TYPE: "camioneta",
  OPTION_MIN_YEAR: 2012,
  OPTION_MAX_PRICE: 65000000,
  OPTION_HAS_ABS_BRAKES: True,
  OPTION_HAS_AIR_CONDITIONING: True,
  OPTION_HAS_POWER_WINDOWS: True,
}

MAX_SCRAPE_PAGES = sys.maxsize
MIN_WAIT_TIME = 10
MAX_WAIT_TIME = 20
