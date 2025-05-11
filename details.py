from playwright.sync_api import sync_playwright
from scraper.field_priority import ordered_fields
from scraper.utils import normalize_number
from scraper.config import *
import csv
import time
import random
import sys
import os

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
                "Año": row["Año"],
                "Ubicación": row["Ubicación"],
                "Enlace": row["Enlace"]
            })
    
    # Read output file if it exists to get already processed cars
    if output_file:
        try:
            with open(output_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if "Enlace" in row:
                        processed_urls.add(row["Enlace"])
        except FileNotFoundError:
            pass  # Output file doesn't exist yet, that's fine
    
    return cars, processed_urls

def get_main_image_url(page):
    """Get the main image URL from the car listing."""
    try:
        # Get all image elements in the gallery
        images = page.locator("#gallery .ui-pdp-gallery__figure__image").all()
        
        # Find the first image that is not a video (doesn't have a video overlay)
        for img in images:
            # Check if the image's parent doesn't have a video overlay
            parent = img.locator("xpath=..")
            if not parent.locator(".clip-wrapper").is_visible():
                # Get the high-resolution image URL from data-zoom attribute
                img_url = img.get_attribute("data-zoom")
                if img_url:
                    return img_url
                
                # Fallback to src attribute if data-zoom is not available
                img_url = img.get_attribute("src")
                if img_url and not img_url.startswith("data:"):
                    return img_url
        
        return None
    except Exception as e:
        print(f"⚠️ Error getting main image: {e}")
        return None

def extract_specs(page):
    """Extract detailed specifications from the car page."""
    specs = {}
    
    # First get the main specifications table
    main_table = page.locator("#technical_specifications .ui-pdp-specs__table")
    if main_table.is_visible():
        rows = main_table.locator(".andes-table__row").all()
        for row in rows:
            name = row.locator(".andes-table__header__container").inner_text()
            value = row.locator(".andes-table__column--value").inner_text()
            
            # Normalize numbers for specific fields
            if name in ["Año", "Kilómetros"]:
                value = normalize_number(value)
            elif name == "Motor":
                # Divide Motor value by 10
                try:
                    value = str(int(normalize_number(value)) / 10)
                except:
                    pass
            
            specs[name] = value
    
    # Try to click the expand button to get more specs
    try:
        expand_button = page.locator("#highlighted_specs_attrs > div.ui-pdp-container__row.ui-pdp-container__row--technical-specifications > div > button")
        if expand_button.is_visible():
            # Smooth scroll to the button
            page.evaluate("""(selector) => {
                const element = document.querySelector(selector);
                if (element) {
                    element.scrollIntoView({ 
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
            }""", "#highlighted_specs_attrs > div.ui-pdp-container__row.ui-pdp-container__row--technical-specifications > div > button")
            
            time.sleep(2)  # Wait for smooth scroll to complete
            
            # Try clicking with JavaScript as a fallback
            try:
                expand_button.click()
            except:
                page.evaluate("""(selector) => {
                    const button = document.querySelector(selector);
                    if (button) button.click();
                }""", "#highlighted_specs_attrs > div.ui-pdp-container__row.ui-pdp-container__row--technical-specifications > div > button")
            
            time.sleep(2)  # Wait for the expanded content
            
            # Get all specification tables
            tables_container = page.locator("#highlighted_specs_attrs > div.ui-pdp-container__row.ui-pdp-container__row--technical-specifications > div > div > div")
            
            # Iterate through all tables
            tables = tables_container.locator("div > div > table").all()
            for table in tables:
                rows = table.locator(".andes-table__row").all()
                for row in rows:
                    name = row.locator(".andes-table__header__container").inner_text()
                    value = row.locator(".andes-table__column--value").inner_text()
                    
                    # Normalize numbers for specific fields
                    if name in ["Año", "Kilómetros"]:
                        value = normalize_number(value)
                    elif name == "Motor":
                        # Divide Motor value by 10
                        try:
                            value = str(int(normalize_number(value)) / 10)
                        except:
                            pass
                    
                    specs[name] = value
    except Exception as e:
        print(f"⚠️ No se pudieron obtener las especificaciones adicionales: {e}")
    
    return specs

def save_to_csv(car_data, filename, fieldnames=None):
    """Save a single car's specifications to a CSV file."""
    if not car_data:
        return
    
    # Always use ordered_fields as the base fieldnames
    fieldnames = ordered_fields
    
    # Check if file exists to determine if we need to write header
    file_exists = os.path.exists(filename)
    
    # Ensure all fields from ordered_fields are present in car_data
    for field in fieldnames:
        if field not in car_data:
            car_data[field] = ""
    
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(car_data)

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
    
    # Limit the number of cars to process
    MIN_LOAD_TIME = 3
    MAX_LOAD_TIME = 6
    cars = cars[:MAX_SCRAPE_PAGES]
    
    print(f"\n🚗 Procesando {len(cars)} carros nuevos...")
    
    with sync_playwright() as p:
        load_time = random.randint(MIN_LOAD_TIME, MAX_LOAD_TIME)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=USER_AGENT, locale="es-CO")
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
                
                # Random delay between cars (10-20 seconds)
                if i < len(cars):  # Don't delay after the last car
                    delay = random.randint(MIN_WAIT_TIME, MAX_WAIT_TIME)
                    print(f"\n⏳ Esperando {delay} segundos...")
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"❌ Error procesando carro {car['Enlace']}: {str(e)}")
                continue
        
        browser.close()
        print(f"\n✅ Proceso completado. Datos guardados en {output_file}")

if __name__ == "__main__": main() 