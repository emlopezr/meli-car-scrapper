import time
import random

def scroll_to_bottom(page):
  """Scroll to the bottom of the page smoothly."""
  page.evaluate("""
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    });
  """)
  # Wait a bit for the scroll to complete
  time.sleep(1)

def has_next_page(page):
  """Check if there is a next page available."""
  scroll_to_bottom(page)
  next_button = page.query_selector('li.andes-pagination__button--next:not(.andes-pagination__button--disabled)')
  return next_button is not None

def navigate_to_next_page(page, min_wait, max_wait):
  """Navigate to the next page if available."""
  try:
    # Check if next button exists and is not disabled
    if not has_next_page(page):
      return False

    # Wait for the next button to be visible and clickable
    next_button = page.wait_for_selector(
      'li.andes-pagination__button--next:not(.andes-pagination__button--disabled)', 
      state="visible", 
      timeout=10000
    )
    
    if next_button:
      wait_time = random.randint(min_wait, max_wait)
      print(f"⏸️  Esperando {wait_time} segundos antes de pasar de página...")
      time.sleep(wait_time)

      # Try to click with force if normal click fails
      try:
        next_button.click()
      except:
        page.evaluate('document.querySelector(\'li.andes-pagination__button--next:not(.andes-pagination__button--disabled)\').click()')
      
      # Wait for navigation to complete
      page.wait_for_load_state("networkidle")
      return True
  except Exception as e:
      print(f"⚠️ Error al navegar a la siguiente página: {e}")
  return False
