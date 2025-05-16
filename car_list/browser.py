from playwright.sync_api import sync_playwright
from utils.config import get_browser_config

def setup_browser():
  """Initialize and return browser context."""
  config = get_browser_config()
  playwright = sync_playwright().start()
  browser = playwright.chromium.launch(headless=config['headless'])
  context = browser.new_context(
    user_agent=config['user_agent'],
    locale=config['locale']
  )
  page = context.new_page()

  return playwright, browser, page

def close_browser(playwright, browser):
  """Close browser and playwright."""
  browser.close()
  playwright.stop()
