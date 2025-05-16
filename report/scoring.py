from models.car import Car
from utils.string_utils import clean_numeric_string, parse_price, parse_engine_size
from utils.config import PRICE_RANGES, YEAR_RANGES, KILOMETER_RANGES, ENGINE_RANGES

def calculate_range_score(value, ranges):
  """Calculate score based on value ranges."""
  for range_config in ranges:
    if range_config.min_value <= value <= range_config.max_value:
      return range_config.points

  return 0

def calculate_year_score(car):
  """Calculate score based on car year."""
  try:
    year = int(car.year)
    return calculate_range_score(year, YEAR_RANGES)
  except (ValueError, TypeError):
    return 0

def calculate_kilometer_score(car):
  """Calculate score based on car kilometers."""
  try:
    km = int(clean_numeric_string(car.km))
    return calculate_range_score(km, KILOMETER_RANGES)
  except (ValueError, TypeError):
    return 0

def calculate_engine_score(car):
  """Calculate score based on engine size."""
  try:
    if not car.engine: return 0
    engine_size = parse_engine_size(car.engine)
    car.engine = str(engine_size)
    return calculate_range_score(engine_size, ENGINE_RANGES)
  except (ValueError, TypeError):
    return 0

def calculate_price_score(car):
  """Calculate score based on car price."""
  try:
    price = parse_price(car.price)
    return calculate_range_score(price, PRICE_RANGES)
  except (ValueError, TypeError):
    return 0

def calculate_car_score(car):
  """Calculate total score for a car."""
  return (
    calculate_year_score(car) +
    calculate_kilometer_score(car) +
    calculate_engine_score(car) +
    calculate_price_score(car)
  )