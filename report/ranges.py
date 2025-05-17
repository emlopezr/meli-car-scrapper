from typing import List
from .types import *

INF = float('inf')

PRICE_RANGES: List[PriceRange] = [
  PriceRange(0,          60_000_000, +8),
  PriceRange(60_000_000, 63_000_000, +6),
  PriceRange(63_000_000, 65_000_000, +4),
  PriceRange(65_000_000, 67_000_000, +1),
  PriceRange(67_000_000, 70_000_000, -3),
  PriceRange(70_000_000, 95_000_000, -5),
]

YEAR_RANGES: List[YearRange] = [
  YearRange(2023, INF,  +5),
  YearRange(2021, 2022, +4),
  YearRange(2019, 2020, +2),
  YearRange(2017, 2018, +1),
]

KILOMETER_RANGES: List[KilometerRange] = [
  KilometerRange(0,       40_000,   +4),
  KilometerRange(40_000,  70_000,   +2),
  KilometerRange(70_000,  90_000,   +0),
  KilometerRange(90_000,  110_000,  -1),
  KilometerRange(110_000, 130_000, -4),
]

KM_PER_YEAR_RANGES: List[KmPerYearRange] = [
  KmPerYearRange(0,      10_000, +4),
  KmPerYearRange(10_000, 15_000, +2),
  KmPerYearRange(15_000, 20_000, +0),
  KmPerYearRange(20_000, 30_000, -2),
  KmPerYearRange(30_000, INF,    -5),
]

ENGINE_RANGES: List[EngineRange] = [
  EngineRange(0.0, 1.6, +4),
  EngineRange(1.6, 2.0, +3),
  EngineRange(2.0, 2.3, +2),
  EngineRange(2.3, INF, +1),
]
