import time
import random

NEXT_BUTTON_SELECTOR = 'li.andes-pagination__button--next:not(.andes-pagination__button--disabled)'

def scroll_to_bottom(page):
  """Scroll to the bottom of the page smoothly."""
  page.evaluate("""
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    });
  """)
  
  time.sleep(1)

def has_next_page(page):
  """Check if there is a next page available."""
  scroll_to_bottom(page)
  next_button = page.query_selector(NEXT_BUTTON_SELECTOR)
  return next_button is not None

def navigate_to_next_page(page, min_wait, max_wait):
  """Navigate to the next page if available."""
  try:
    if not has_next_page(page): return False

    next_button = page.wait_for_selector(
      NEXT_BUTTON_SELECTOR, 
      state="visible", 
      timeout=10000
    )
    
    if next_button:
      wait_time = random.randint(min_wait, max_wait)
      print(f"⌛ Esperando {wait_time} segundos antes de pasar de página...")
      time.sleep(wait_time)

      try:
        next_button.click()
      except:
        page.evaluate('document.querySelector(\'li.andes-pagination__button--next:not(.andes-pagination__button--disabled)\').click()')
      
      page.wait_for_load_state("networkidle")

      return True
    
  except Exception as e:
      print(f"⚠️ Error al navegar a la siguiente página: {e}")
  
  return False
