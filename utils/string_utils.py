def parse_numeric_string(value: str, allow_decimal: bool = True, handle_currency: bool = False) -> float:
  if not value: return 0.0

  # Handle currency cases
  if handle_currency:
    value = value.replace('$', '').strip().lower()
    if 'm' in value: return float(value.replace('m', '')) * 1_000_000

  # Remove commas and spaces
  value = value.replace(',', '').replace(' ', '')

  # Filter characters based on allow_decimal
  if allow_decimal: value = ''.join(c for c in value if c.isdigit() or c == '.')
  else: value = ''.join(c for c in value if c.isdigit())

  return float(value) if value else 0.0

def parse_engine_size(engine_str: str) -> float:
  """Parse engine size string to float value."""
  engine_str = engine_str.lower().strip()
  if "bv cxv" in engine_str: return 3.5

  cleaned = parse_numeric_string(engine_str)
  if not cleaned: raise ValueError("Invalid engine size")

  engine_float = float(cleaned)
  if engine_float > 1000: engine_float /= 1000
  if engine_float > 10: engine_float /= 100

  return round(engine_float, 1)
