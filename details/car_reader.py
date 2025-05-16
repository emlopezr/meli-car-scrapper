import csv

def read_cars_from_csv(filename, output_file=None):
  """Read car URLs from the CSV file created in the first stage and check already processed cars."""
  cars = []
  processed_urls = set()

  # Read input file
  with open(filename, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
      cars.append({
        "Título": row["Título"],
        "Precio": row["Precio"],
        "Enlace": row["Enlace"]
      })

  # Read output file if it exists to get already processed cars
  if output_file:
    try:
      with open(output_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
          if "Enlace" in row: processed_urls.add(row["Enlace"])

    except FileNotFoundError: pass

  return cars, processed_urls

def filter_processed_cars(cars, processed_urls):
  """Filter out already processed cars from the list."""
  return [car for car in cars if car["Enlace"] not in processed_urls]
