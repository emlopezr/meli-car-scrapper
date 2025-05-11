from playwright.sync_api import sync_playwright
import csv
import time
import re
import random
import sys
from scraper.config import *
from scraper.field_priority import priority_fields

def normalize_number(text):
  """Convert text to number by removing non-digit characters."""
  return int(''.join(c for c in text if c.isdigit())) if text else 0

def read_cars_from_csv(filename):
    """Read car URLs from the CSV file created in the first stage."""
    cars = []
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
    return cars

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

def save_to_csv(cars_with_specs, filename):
    """Save car specifications to a CSV file."""
    if not cars_with_specs: return
    
    # Get all possible field names from all cars
    fieldnames = set()
    for car in cars_with_specs:
        fieldnames.update(car.keys())
    
    # Convert to list and sort remaining fields alphabetically
    remaining_fields = sorted(list(fieldnames - set(priority_fields)))
    
    # Combine priority fields with remaining fields
    # Only include priority fields that exist in the data
    fieldnames = [field for field in priority_fields if field in fieldnames] + remaining_fields
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cars_with_specs)

def main():
    # Read cars from the first stage output
    cars = read_cars_from_csv(CSV_LIST)
    
    # Randomly shuffle the list before processing
    random.shuffle(cars)
    
    # Limit the number of cars to process
    MAX_CARS = sys.maxsize  # Maximum integer value
    cars = cars[:MAX_CARS]
    
    print(f"\n🚗 Procesando {len(cars)} carros...")
    
    # Initialize list to store processed cars
    cars_with_specs = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=REAL_USER_AGENT, locale="es-CO")
        page = context.new_page()

        # First visit the last car to initialize the structure
        if len(cars) > 1:
            last_car = cars[-1]
            page.goto(last_car['Enlace'])
            time.sleep(random.randint(4,8))  # Wait for the page to fully load

        # Process each car
        for i, car in enumerate(cars, 1):
            print(f"\n🔍 Procesando carro {i} de {len(cars)}: {car['Título']}")
            print(f"📎 URL: {car['Enlace']}")
            
            page.goto(car['Enlace'])
            time.sleep(random.randint(2,5))  # Wait for the page to load
            
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
            cars_with_specs.append(car_data)
            
            # Print specifications
            print("\n📋 Especificaciones:")
            for name, value in specs.items():
                print(f"{name}: {value}")
            
            # Random delay between cars (10-20 seconds)
            if i < len(cars):  # Don't delay after the last car
                delay = random.randint(10, 20)
                print(f"\n⏳ Esperando {delay} segundos...")
                time.sleep(delay)
        
        # Save all data to CSV
        save_to_csv(cars_with_specs, CSV_DETAILS)
        print(f"\n✅ Datos guardados en {CSV_DETAILS}")
        
        browser.close()

if __name__ == "__main__": main() 