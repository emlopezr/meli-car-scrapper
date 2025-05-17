import os
from .exporter import read_existing_cars, save_to_csv

def load_existing_cars(output_file, append_mode):
  """Load existing cars if in append mode."""
  if not append_mode: return set()

  try:
    existing_cars = read_existing_cars(output_file)
    print(f"\n📊 Modo: Añadir")
    print(f"📄 Carros existentes: {len(existing_cars)}")
    return existing_cars

  except FileNotFoundError:
    print("\n📊 Modo: Añadir")
    print("📄 No hay carros existentes")
    return set()

def process_results(existing_cars, new_cars, append_mode):
  """Process and combine results based on mode."""
  if append_mode:
    all_cars = existing_cars.union(new_cars)
    print(f"\n🆕 Carros nuevos encontrados: {len(new_cars)}")
    print(f"📈 Carros duplicados ignorados: {len(existing_cars) + len(new_cars) - len(all_cars)}")
  else:
    all_cars = new_cars
    print(f"🆕 Carros encontrados: {len(new_cars)}")

  return list(all_cars)

def save_results(cars, output_file):
  """Save results to CSV file."""
  # Create directory if it doesn't exist and file is not in current directory
  directory = os.path.dirname(output_file)
  if directory: os.makedirs(directory, exist_ok=True)

  save_to_csv(cars, output_file)
  print(f"\n✅ Datos guardados en {output_file} con {len(cars)} registros.")
