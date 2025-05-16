from .image_extractor import get_main_image_url
from .specs_extractor import extract_specs

def process_car(page, car: dict, load_time: int) -> dict:
  """Process a single car listing and return its data."""
  print(f"\n🔍 Procesando carro: {car['Título']}")
  print(f"📎 URL: {car['Enlace'].split('-_JM')[0]}")

  try:
    page.goto(car['Enlace'])
    wait_for_page(load_time)

    main_image = get_main_image_url(page)
    if main_image: print(f"🖼️ Imagen principal: {main_image}")

    specs = extract_specs(page)
    return build_car_data(car, main_image, specs)

  except Exception as e:
    print(f"❌ Error procesando carro {car['Enlace']}: {str(e)}")
    return {}

def wait_for_page(load_time: int):
  import time
  time.sleep(load_time)

def build_car_data(car: dict, main_image: str, specs: dict) -> dict:
  data = {
    "Título": car.get("Título", ""),
    "Precio": car.get("Precio", ""),
    "Enlace": car.get("Enlace", ""),
    "Ubicación": car.get("Ubicación", ""),
    "ImagenURL": main_image,
    **specs
  }
  return data
