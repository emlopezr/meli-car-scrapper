def get_main_image_url(page):
  """Get the main image URL from the car listing."""
  try:
    # Get all image elements in the gallery
    images = page.locator("#gallery .ui-pdp-gallery__figure__image").all()

    # Find the first image that is not a video
    for img in images:
      parent = img.locator("xpath=..")

      if not parent.locator(".clip-wrapper").is_visible():
        # Try high-res image first
        img_url = img.get_attribute("data-zoom")
        if img_url: return img_url

        # Fallback to src attribute
        img_url = img.get_attribute("src")
        if img_url and not img_url.startswith("data:"): return img_url

    return None

  except Exception as e:
    print(f"⚠️ Error getting main image: {e}")
    return None
