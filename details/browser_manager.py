from playwright.sync_api import sync_playwright
from utils.config import get_browser_config
import time

def create_browser_context():
  """Create and return a browser context with the configured user agent."""
  config = get_browser_config()
  p = sync_playwright().start()
  browser = p.chromium.launch(headless=False)

  context = browser.new_context(
    user_agent=config['user_agent'],
    locale=config['locale'],
  )

  page = context.new_page()

  return p, browser, context, page

def load_page(page, url, load_time):
  """Load a URL in the existing page and wait for the specified time."""
  page.goto(url)
  time.sleep(load_time)
  return page 