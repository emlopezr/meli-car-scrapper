import json
import os

def load_config():
  """Load configuration from JSON file."""
  config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
  with open(config_path, 'r') as f:
    return json.load(f)

def get_browser_config():
  """Get browser configuration."""
  config = load_config()
  return config['browser']

def get_scraping_config():
  """Get scraping configuration."""
  config = load_config()
  return config['scraping'] 