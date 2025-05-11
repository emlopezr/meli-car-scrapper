import csv
from model.car import Car

def read_existing_cars(filename):
    """Read existing cars from CSV file."""
    cars = set()

    try:
      with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
          car = Car(
            title=row["Título"],
            price=int(row["Precio"]),
            year=int(row["Año"]),
            km=int(row["Kilometraje"]),
            link=row["Enlace"],
            location=row["Ubicación"]
          )
          
          cars.add(car)

    except FileNotFoundError:
      print("📄 No se encontró archivo existente, se creará uno nuevo.")

    return cars

def save_to_csv(cars, filename):
    """Save cars to CSV file."""
    if not cars: return

    fieldnames = ["Título", "Precio", "Año", "Kilometraje", "Enlace", "Ubicación"]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writeheader()
      
      for car in cars:
        writer.writerow({
          "Título": car.title,
          "Precio": car.price,
          "Año": car.year,
          "Kilometraje": car.km,
          "Enlace": car.link,
          "Ubicación": car.location
        })
