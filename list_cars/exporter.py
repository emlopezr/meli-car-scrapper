import csv
from models.car import Car
from utils.string_utils import parse_numeric_string
from utils.constants import CSV_FIELDNAMES, COLUMN_TITLE, COLUMN_PRICE, COLUMN_LINK

def read_existing_cars(filename):
  """Read existing cars from CSV file."""
  cars = set()

  try:
    with open(filename, mode="r", encoding="utf-8") as file:
      reader = csv.DictReader(file)

      for row in reader:
        car = Car(
          title=row[COLUMN_TITLE],
          price=int(parse_numeric_string(row[COLUMN_PRICE])),
          link=row[COLUMN_LINK]
        )

        cars.add(car)

  except FileNotFoundError:
    print("📄 No se encontró archivo existente, se creará uno nuevo.")

  return cars

def save_to_csv(cars, filename):
  """Save cars to CSV file."""
  if not cars: return

  with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
    writer.writeheader()
    
    for car in cars:
      writer.writerow({
        COLUMN_TITLE: car.title,
        COLUMN_PRICE: car.price,
        COLUMN_LINK: car.link
      }) 