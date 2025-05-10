import csv

def save_to_csv(cars, filename):
  """Save the car data to a CSV file."""
  with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Título", "Precio", "Año", "Kilometraje", "Ubicación", "Enlace", "Score"])
    for car in cars:
      writer.writerow([
          car.title,
          car.price,
          car.year,
          car.km,
          car.location,
          car.link,
          car.score
      ])
