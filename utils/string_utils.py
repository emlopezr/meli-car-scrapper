def parse_numeric_string(value: str) -> int:
  """Extract all numeric characters from a string and convert to integer."""
  if not value: return 0
  return int(''.join(c for c in value if c.isdigit()))

def parse_engine_size(engine_str: str) -> float:
  """Parse engine size string to float value."""
  engine_str = engine_str.lower().strip()
  if "bv cxv" in engine_str: return 3.5

  cleaned = parse_numeric_string(engine_str)
  if not cleaned: raise ValueError("Invalid engine size")

  engine_float = float(cleaned)
  if engine_float >= 1000: engine_float /= 1000
  if engine_float >= 100: engine_float /= 100
  if engine_float >= 10: engine_float /= 10

  return round(engine_float, 1)
