import sys
import random
from utils.config import get_scraping_config
from details.car_reader import read_cars_from_csv, filter_processed_cars
from details.csv_writer import save_to_csv
from details.browser_manager import create_browser_context, load_page
from details.car_processor import process_car

def print_specs(car_data: dict):
  print("\n📋 Especificaciones:")
  for name, value in car_data.items():
    if name not in ["Título", "Precio", "Enlace", "ImagenURL"]:
      print(f"{name}: {value}")

def main():
  if len(sys.argv) != 3:
    print("Usage: python -m details.py <input_file> <output_file>")
    return

  input_file = sys.argv[1]
  output_file = sys.argv[2]

  cars, processed_urls = read_cars_from_csv(input_file, output_file)
  cars = filter_processed_cars(cars, processed_urls)

  if not cars:
    print("\n✅ No hay carros nuevos para procesar.")
    return

  config = get_scraping_config()
  max_cars = config.get('max_pages', sys.maxsize)
  min_wait = config['min_wait_time']
  max_wait = config['max_wait_time']

  cars = cars[:max_cars]
  random.shuffle(cars)

  print(f"\n🚗 Procesando {len(cars)} carros nuevos...")
  p, browser, context, page = create_browser_context()
  load_time = random.randint(3, 6)

  try:
    if len(cars) > 0:
      load_page(page, cars[-1]['Enlace'], load_time)
      import time; time.sleep(5)

    for i, car in enumerate(cars, 1):
      load_page(page, car['Enlace'], load_time)
      print(f"\n========== {i}/{len(cars)} ==========")
      car_data = process_car(page, car, load_time)

      if car_data:
        save_to_csv(car_data, output_file)
        print("✅ Carro guardado exitosamente")
        print_specs(car_data)

      if i < len(cars):
        delay = random.randint(min_wait, max_wait)
        print(f"\n⏳ Esperando {delay} segundos...")
        import time; time.sleep(delay)

  finally:
    browser.close()
    p.stop()

  print(f"\n✅ Proceso completado. Datos guardados en {output_file}")

if __name__ == "__main__": main()