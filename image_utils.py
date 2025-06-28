import base64

def image_to_base64(image_path):
    """
    Convert an image to a base64-encoded string.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"[Base64 Conversion Error] {image_path}: {e}")
        return None
