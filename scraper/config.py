import sys

BASE_URL = "https://carros.mercadolibre.com.co"

REAL_USER_AGENT = (
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
  "Chrome/124.0.6367.61 Safari/537.36"
)

SEARCH_OPTIONS = {
  "gear": "automatica",
  "type": "camioneta",
  # "location": "antioquia",
  "min_year": 2012,
  "max_price": 65000000,
  "has_abs_brakes": True,
  "has_air_conditioning": True,
  "has_power_windows": True,
}

MAX_PAGES = sys.maxsize  # Maximum integer value
MIN_WAIT_TIME = 30
MAX_WAIT_TIME = 60

CSV_LIST = "output_list.csv"
CSV_DETAILS = "output_details.csv"
