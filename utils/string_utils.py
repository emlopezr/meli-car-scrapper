def clean_numeric_string(value: str) -> str:
  """Clean a numeric string by removing non-numeric characters."""
  return ''.join(c for c in value if c.isdigit() or c == '.')

def normalize_number(text):
  """Convert text to number by removing non-digit characters."""
  return int(''.join(c for c in text if c.isdigit())) if text else 0

def parse_price(price_str: str) -> float:
  """Parse price string to float value."""
  price_str = price_str.replace('.', '').replace(',', '').replace('$', '').strip().lower()

  if 'm' in price_str: return float(price_str.replace('m', '')) * 1_000_000
  return float(price_str)

def parse_engine_size(engine_str: str) -> float:
  """Parse engine size string to float value."""
  engine_str = engine_str.lower().strip()
  if "bv cxv" in engine_str: return 3.5

  cleaned = clean_numeric_string(engine_str)
  if not cleaned: raise ValueError("Invalid engine size")

  engine_float = float(cleaned)
  if engine_float > 1000: engine_float /= 1000
  if engine_float > 10: engine_float /= 100

  return round(engine_float, 1)
