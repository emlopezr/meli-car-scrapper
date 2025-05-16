import time
from utils.string_utils import normalize_number

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

def normalize_spec_value(name, value):
  """Normalize specification values based on field type."""
  if name in ["Año", "Kilómetros"]:
    return normalize_number(value)
  elif name == "Motor":
    try: return str(int(normalize_number(value)) / 10)
    except: return value
  return value

def scroll_to_element(page, element):
  """Smooth scroll to an element."""
  page.evaluate("""(selector) => {
    const element = document.querySelector(selector);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      });
    }
  }""", element)

def click_with_js(page, element):
  """Click an element using JavaScript."""
  page.evaluate("""(selector) => {
    const button = document.querySelector(selector);
    if (button) button.click();
  }""", element)
