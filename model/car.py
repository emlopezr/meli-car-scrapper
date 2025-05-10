class Car:
  def __init__(self, title, price, year, km, link, location):
    self.title = title
    self.price = price
    self.year = year
    self.km = km
    self.link = link
    self.location = location
    self.score = 0

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
