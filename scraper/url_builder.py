from .config import BASE_URL

def build_url(options):
  """Build the search URL based on the provided options."""
  filters = []
  filters.append(options['gear'])
  
  if options.get('gear', False): filters.append(options.get('gear'))
  if options.get('has_abs_brakes', False): filters.append('con-frenos-abs')
  if options.get('has_air_conditioning', False): filters.append('con-aire-acondicionado')
  if options.get('has_power_windows', False): filters.append('con-vidrios-electricos')
  if options.get('type', False): filters.append(options.get('type'))
  if options.get('location', False): filters.append(options.get('location'))
  
  url = f"{BASE_URL}/{'/'.join(filters)}/desde-{options['min_year']}/"
  url += f"_PriceRange_0-{options['max_price']}"
  url += "_NoIndex_True" 
  
  return url
