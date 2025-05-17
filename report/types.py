"""Type definitions for car scoring configuration."""

class CarScore:
  """Base class for car scoring configuration."""
  def __init__(self, min_value, max_value, points):
    self.min_value = min_value
    self.max_value = max_value
    self.points = points

class PriceRange(CarScore): pass
class YearRange(CarScore): pass
class KilometerRange(CarScore): pass
class EngineRange(CarScore): pass
class KmPerYearRange(CarScore): pass