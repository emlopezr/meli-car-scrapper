import csv
import sys
from scraper.field_priority import ordered_fields

def read_cars_from_csv(filename):
    """Read cars from the CSV file."""
    cars = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cars.append(row)
    return cars

def calculate_car_score(car):
    """Calcula un puntaje total del carro basado solo en los campos disponibles del scraper."""
    score = 0

    def has_feature(value):
        return str(value).strip().lower() in ['sí', 'si', 'yes', 'true', '1']

    # ⚙️ Características principales con peso
    features = {
        "Airbag conductor": 5,
        "Airbag para conductor y pasajero": 5,
        "Frenos ABS": 5,
        "Control de estabilidad": 5,
        "Aire acondicionado": 4,
        "Climatizador": 3,
        "Sensor de parqueo": 2,
        "Con cámara de reversa": 2,
        "Bluetooth": 2,
        "Entrada USB": 1,
        "Techo corredizo": 3,
        "Tapizado de cuero": 2,
        "Llantas de aleación": 2,
        "Cierre centralizado de puertas": 2,
        "Vidrios eléctricos": 2,
        "Computadora de abordo": 1,
        "Comando remoto para radio en el volante": 1,
        "Sensor de lluvia": 1,
        "Piloto automático": 1,
        "Con garantía de fábrica": 4,
        "Con garantía mecánica": 3,
        "Con precio negociable": 1,
        "Venpermuta": 1,
        "Único dueño": 2
    }

    for field, pts in features.items():
        if has_feature(car.get(field)): score += pts

    # 📅 Año del vehículo
    try:
        year = int(car.get('Año', 0))
        if year >= 2021: score += 8
        elif year >= 2019: score += 5
        elif year >= 2017: score += 3
        elif year >= 2015: score += 1
    except:
        pass

    # 🛣️ Kilometraje
    try:
        km = int(str(car.get('Kilómetros', '0')).replace('.', '').replace(',', '').strip())
        if km <= 35000: score += 8
        elif km <= 50000: score += 5
        elif km <= 75000: score += 3
        elif km <= 90000: score += 1
    except:
        pass

    # 🔧 Tamaño del motor (menos consumo = más puntos)
    try:
        motor_str = str(car.get("Motor", "")).lower().replace('l', '').strip()
        motor_float = float(motor_str)
        if motor_float <= 1.6: score += 5
        elif motor_float <= 2.0: score += 2
        elif motor_float <= 2.3: score -= 1
        elif motor_float <= 2.6: score -= 3
        # Motores grandes no suman
    except:
        pass
      
    # 💰 Precio (entre menor, mejor)
    try:
        precio_str = str(car.get('Precio', '0')).replace('.', '').replace(',', '').replace('$', '').strip().lower()
        if 'm' in precio_str: precio = float(precio_str.replace('m', '')) * 1_000_000
        else: precio = float(precio_str)

        if precio <= 40_000_000: score += 8
        elif precio <= 45_000_000: score += 6
        elif precio <= 50_000_000: score += 4
        elif precio <= 55_000_000: score += 3
        elif precio <= 60_000_000: score += 1
    except:
        pass

    return score

def save_to_csv(cars, filename):
    """Save cars to CSV with sorted columns."""
    if not cars: return
    
    # Get all possible field names from all cars
    fieldnames = set()
    for car in cars:
        fieldnames.update(car.keys())
    
    # Sort remaining fields alphabetically
    remaining_fields = sorted(list(fieldnames - set(ordered_fields)))
    
    # Combine ordered fields with remaining fields
    # Only include ordered fields that exist in the data
    final_fieldnames = [field for field in ordered_fields if field in fieldnames] + remaining_fields
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=final_fieldnames)
        writer.writeheader()
        writer.writerows(cars)

def main():
    if len(sys.argv) != 3:
        print("Usage: python process_cars.py input.csv output.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read cars from input CSV
    cars = read_cars_from_csv(input_file)
    print(f"\n🚗 Procesando {len(cars)} carros...")
    
    # Calculate score for each car
    for car in cars:
        score = calculate_car_score(car)
        car['Score'] = score
        print(f"📊 {car['Título']}: {score} puntos")
    
    # Save to output CSV with sorted columns
    save_to_csv(cars, output_file)
    print(f"\n✅ Datos procesados y guardados en {output_file}")

if __name__ == "__main__":
    main() 