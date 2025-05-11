def normalize_number(text):
  """Convert text to number by removing non-digit characters."""
  return int(''.join(c for c in text if c.isdigit())) if text else 0