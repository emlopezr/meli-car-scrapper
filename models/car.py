from dataclasses import dataclass

@dataclass
class Car:
  """Core Car model representing a vehicle."""
  title: str
  price: str
  year: str
  km: str
  link: str
  location: str
  score: int = 0
  engine: str = None

  def __eq__(self, other):
    """Two cars are considered equal if they have the same title, price, year and kilometers."""
    if not isinstance(other, Car): return False
    return (
      self.title == other.title and
      self.price == other.price and
      self.year == other.year and
      self.km == other.km
    )

  def __hash__(self):
    """Hash based on the attributes that determine equality."""
    return hash((self.title, self.price, self.year, self.km))
