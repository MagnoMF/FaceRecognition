import base64

def is_base64(base_64: str) -> bool:
    try:
        base64.b64decode(base_64, validate=True)
        return True
    except:
        return False