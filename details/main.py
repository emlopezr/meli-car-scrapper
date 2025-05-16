import sys
import random
import time
from playwright.sync_api import sync_playwright
from utils.config import get_scraping_config
from .car_reader import read_cars_from_csv
from .image_extractor import get_main_image_url
from .specs_extractor import extract_specs
from .csv_writer import save_to_csv

def main():
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  
  # Read cars from the first stage output and get already processed URLs
  cars, processed_urls = read_cars_from_csv(input_file, output_file)
  
  # Filter out already processed cars
  cars = [car for car in cars if car['Enlace'] not in processed_urls]
  
  if not cars:
    print("\n✅ No hay carros nuevos para procesar.")
    return
  
  # Randomly shuffle the list before processing
  random.shuffle(cars)
  
  # Get config
  config = get_scraping_config()
  max_cars = config['max_pages']
  min_wait = config['min_wait_time']
  max_wait = config['max_wait_time']
  user_agent = config['browser']['user_agent']
  
  # Limit the number of cars to process
  MIN_LOAD_TIME = 3
  MAX_LOAD_TIME = 6
  cars = cars[:max_cars]
  
  print(f"\n🚗 Procesando {len(cars)} carros nuevos...")
  
  with sync_playwright() as p:
    load_time = random.randint(MIN_LOAD_TIME, MAX_LOAD_TIME)
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(user_agent=user_agent, locale="es-CO")
    page = context.new_page()

    # First visit the last car to initialize the structure
    if len(cars) > 1:
      last_car = cars[-1]
      page.goto(last_car['Enlace'])
      time.sleep(load_time)

    # Process each car
    for i, car in enumerate(cars, 1):
      print(f"\n🔍 Procesando carro {i} de {len(cars)}: {car['Título']}")
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
        
        # Combine car info with specs, keeping basic info first
        car_data = {
          # Basic info from first stage
          "Título": car["Título"],
          "Precio": car["Precio"],
          "Año": car["Año"],
          "Ubicación": car["Ubicación"],
          "Enlace": car["Enlace"],
          "ImagenURL": main_image,
          # Additional specs from second stage
          **specs
        }
        
        # Save car data immediately
        save_to_csv(car_data, output_file)
        print("✅ Carro guardado exitosamente")
        
        # Print specifications
        print("\n📋 Especificaciones:")
        for name, value in specs.items():
          print(f"{name}: {value}")
        
        # Random delay between cars
        if i < len(cars):  # Don't delay after the last car
          delay = random.randint(min_wait, max_wait)
          print(f"\n⏳ Esperando {delay} segundos...")
          time.sleep(delay)
          
      except Exception as e:
        print(f"❌ Error procesando carro {car['Enlace']}: {str(e)}")
        continue
    
    browser.close()
    print(f"\n✅ Proceso completado. Datos guardados en {output_file}")

if __name__ == "__main__":
  main() 