from models.car import Car
from utils.string_utils import parse_numeric_string, parse_engine_size
from report.ranges import *

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
from datetime import datetime

def calculate_kilometer_score(car):
  """Calculate score based on kilometers per year."""
  try:
    km = int(parse_numeric_string(car.km))
    year = int(car.year)

    current_year = datetime.now().year
    years_of_use = max(current_year - year, 1)

    km_per_year = km / years_of_use

    return calculate_range_score(km_per_year, KM_PER_YEAR_RANGES)
  except (ValueError, TypeError, ZeroDivisionError):
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
    price = parse_numeric_string(car.price)
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