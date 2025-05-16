import csv
import os
from utils.constants import FIELD_PRIORITY

def save_to_csv(car_data, filename, fieldnames=None):
  """Save a single car's specifications to a CSV file."""
  if not car_data: return

  # Always use FIELD_PRIORITY as the base fieldnames
  fieldnames = FIELD_PRIORITY

  # Check if file exists to determine if we need to write header
  file_exists = os.path.exists(filename)

  # Ensure all fields from FIELD_PRIORITY are present in car_data
  for field in fieldnames:
    if field not in car_data:
      car_data[field] = ""

  with open(filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if not file_exists:
      writer.writeheader()
    writer.writerow(car_data)
