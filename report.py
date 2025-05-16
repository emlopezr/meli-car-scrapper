import sys
from report.csv_service import read_cars_from_csv, save_to_csv
from report.scoring import calculate_car_score
from models.car import Car

def process_cars(cars):
  """Process cars by calculating their scores."""
  for car in cars:
    score = calculate_car_score(car)
    car.score = score
    print(f"📊 {car.title}: {score} puntos")

def main():
  if len(sys.argv) != 3:
    print("Usage: py report.py input.csv output.csv")
    sys.exit(1)

  input_file = sys.argv[1]
  output_file = sys.argv[2]

  cars = read_cars_from_csv(input_file)
  print(f"\n🚗 Procesando {len(cars)} carros...")

  process_cars(cars)
  save_to_csv(cars, output_file)
  print(f"\n✅ Datos procesados y guardados en {output_file}")

if __name__ == "__main__":
  main()
