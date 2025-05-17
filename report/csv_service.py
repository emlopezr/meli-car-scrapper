import csv
from models.car import Car
from utils.constants import FIELD_PRIORITY

def read_cars_from_csv(filename):
  """Read cars from the CSV file."""
  cars = []
  original_headers = []

  with open(filename, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    original_headers = reader.fieldnames

    for row in reader:
      car = Car(
        title=row.get('Título', ''),
        price=row.get('Precio', ''),
        year=row.get('Año', ''),
        km=row.get('Kilómetros', ''),
        link=row.get('Link', ''),
        location=row.get('Ubicación', ''),
        engine=row.get('Motor', '')
      )
      # Store all original data
      car.original_data = row
      cars.append(car)

  return cars, original_headers

def get_fieldnames(cars):
  """Get sorted fieldnames from cars data."""
  fieldnames = set()

  for car in cars:
    fieldnames.update(car.__dict__.keys())

  remaining_fields = sorted(list(fieldnames - set(FIELD_PRIORITY)))
  return [field for field in FIELD_PRIORITY if field in fieldnames] + remaining_fields

def save_to_csv(cars, filename, original_headers):
  """Save cars to CSV preserving all original columns and adding score at the start."""
  if not cars: return

  # Add score as the first column
  fieldnames = ['Score'] + list(original_headers)

  with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for car in cars:
      row_data = car.original_data.copy()
      row_data['Score'] = car.score
      writer.writerow(row_data)
