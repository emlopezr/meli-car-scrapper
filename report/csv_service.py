import csv
from models.car import Car
from car_list.constants import FIELD_PRIORITY

def read_cars_from_csv(filename):
  """Read cars from the CSV file."""
  cars = []

  with open(filename, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
      cars.append(Car(
        title=row.get('Título', ''),
        price=row.get('Precio', ''),
        year=row.get('Año', ''),
        km=row.get('Kilómetros', ''),
        link=row.get('Link', ''),
        location=row.get('Ubicación', ''),
        engine=row.get('Motor', '')
      ))

  return cars

def get_fieldnames(cars):
  """Get sorted fieldnames from cars data."""
  fieldnames = set()

  for car in cars:
    fieldnames.update(car.__dict__.keys())

  remaining_fields = sorted(list(fieldnames - set(FIELD_PRIORITY)))
  return [field for field in FIELD_PRIORITY if field in fieldnames] + remaining_fields

def save_to_csv(cars, filename):
  """Save cars to CSV with sorted columns."""
  if not cars: return

  fieldnames = get_fieldnames(cars)

  with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([car.__dict__ for car in cars]) 