import random
import time
from .config import get_scraping_config

def scroll_to_bottom(page):
  """Scroll to bottom of page to load all content."""
  page.evaluate("""
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    });
  """)
  time.sleep(random.randint(1, 2))

def navigate_to_next_page(page):
  """Navigate to next page if available."""
  config = get_scraping_config()
  min_wait = config['min_wait_time']
  max_wait = config['max_wait_time']

  try:
    # Scroll to bottom first to ensure all content is loaded
    scroll_to_bottom(page)
    next_button = page.query_selector("li.andes-pagination__button--next:not(.andes-pagination__button--disabled)")
    if not next_button: return False

    next_button.click()
    sleep_time = random.randint(min_wait, max_wait)
    print(f"\n⌛ Esperando {sleep_time} segundos...")
    time.sleep(sleep_time)
    return True

  except Exception as e:
    print(f"❌ Error navegando a siguiente página: {e}")
    return False