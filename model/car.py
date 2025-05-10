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

    def to_dict(self):
        """Convert car data to dictionary format."""
        return {
            "title": self.title,
            "price": self.price,
            "year": self.year,
            "km": self.km,
            "link": self.link,
            "location": self.location,
            "score": self.score
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Car instance from a dictionary."""
        car = cls(
            title=data["title"],
            price=data["price"],
            year=data["year"],
            km=data["km"],
            link=data["link"],
            location=data["location"]
        )
        car.score = data.get("score", 0)
        return car 