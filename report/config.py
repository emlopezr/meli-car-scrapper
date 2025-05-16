from typing import List
from .types import PriceRange, YearRange, KilometerRange, EngineRange

PRICE_RANGES: List[PriceRange] = [
  PriceRange(0, 40_000_000, 8),
  PriceRange(40_000_000, 45_000_000, 6),
  PriceRange(45_000_000, 50_000_000, 4),
  PriceRange(50_000_000, 55_000_000, 3),
  PriceRange(55_000_000, 60_000_000, 1)
]

YEAR_RANGES: List[YearRange] = [
  YearRange(2021, float('inf'), 8),
  YearRange(2019, 2020, 5),
  YearRange(2017, 2018, 3),
  YearRange(2015, 2016, 1)
]

KILOMETER_RANGES: List[KilometerRange] = [
  KilometerRange(0, 35000, 8),
  KilometerRange(35000, 50000, 5),
  KilometerRange(50000, 75000, 3),
  KilometerRange(75000, 90000, 1)
]

ENGINE_RANGES: List[EngineRange] = [
  EngineRange(0, 1.6, 5),
  EngineRange(1.6, 2.0, 2),
  EngineRange(2.0, 2.3, -1),
  EngineRange(2.3, 2.6, -3)
]
