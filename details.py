import sys
import random
import time
from utils.config import get_scraping_config
from details.car_reader import read_cars_from_csv, filter_processed_cars
from details.image_extractor import get_main_image_url
from details.specs_extractor import extract_specs
from details.csv_writer import save_to_csv
from details.browser_manager import create_browser_context, load_page
import csv
import os

def process_car(page, car, load_time):
  """Process a single car listing."""
  print(f"\n🔍 Procesando carro: {car['Título']}")
  print(f"📎 URL: {car['Enlace'].split('-_JM')[0]}")
  
  try:
    page.goto(car['Enlace'])
    time.sleep(load_time)
    
    # Get main image URL
    main_image = get_main_image_url(page)
    if main_image:
      print(f"🖼️ Imagen principal: {main_image}")
    
    # Extract specifications
    specs = extract_specs(page)
    
    # Combine car info with specs
    car_data = {
      "Título": car["Título"],
      "Precio": car["Precio"],
      "Enlace": car["Enlace"],
      "Año": 0,
      "Ubicación": "TO-DO",
      "ImagenURL": main_image,
      **specs
    }
    
    return car_data
    
  except Exception as e:
    print(f"❌ Error procesando carro {car['Enlace']}: {str(e)}")
    return None

def main():
  if len(sys.argv) != 3:
    print("Usage: python -m details.main <input_file> <output_file>")
    return
    
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  
  # Read and filter cars
  cars, processed_urls = read_cars_from_csv(input_file, output_file)
  cars = filter_processed_cars(cars, processed_urls)
  
  if not cars:
    print("\n✅ No hay carros nuevos para procesar.")
    return
  
  # Get config
  config = get_scraping_config()
  max_cars = config['max_pages']
  min_wait = config['min_wait_time']
  max_wait = config['max_wait_time']
  
  # Limit and shuffle cars
  cars = cars[:max_cars]
  random.shuffle(cars)
  
  print(f"\n🚗 Procesando {len(cars)} carros nuevos...")
  
  # Initialize browser
  p, browser, context, page = create_browser_context()
  load_time = random.randint(3, 6)
  
  try:
    # Visit the last car in the list to initialize the structure
    if len(cars) > 0:
      load_page(page, cars[-1]['Enlace'], load_time)
      time.sleep(5)  # Wait 5 seconds for the last car
    
    # Process each car in the original order
    for i, car in enumerate(cars, 1):
      load_page(page, car['Enlace'], load_time)
      car_data = process_car(page, car, load_time)
      
      if car_data:
        save_to_csv(car_data, output_file)
        print("✅ Carro guardado exitosamente")
        
        # Print specifications
        print("\n📋 Especificaciones:")
        for name, value in car_data.items():
          if name not in ["Título", "Precio", "Año", "Ubicación", "Enlace", "ImagenURL"]:
            print(f"{name}: {value}")
      
      # Random delay between cars
      if i < len(cars):
        delay = random.randint(min_wait, max_wait)
        print(f"\n⏳ Esperando {delay} segundos...")
        time.sleep(delay)
        
  finally:
    browser.close()
    p.stop()
    
  print(f"\n✅ Proceso completado. Datos guardados en {output_file}")

if __name__ == "__main__":
  main() 