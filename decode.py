import png
import base64
import json

def read_metadata(file_path: str) -> str:
    with open(file_path, "rb") as f:
        r = png.Reader(file=f)
        for chunk in r.chunks():
            if chunk[0] == b"tEXt":
                key, value = chunk[1].split(b'\x00', 1)
                if key == b"chara":
                    result: str = value.decode("utf-8", errors="replace")
                    return result
        else:
            return ""

def decode_base64(data: str):
    try:
        decoded_data = base64.b64decode(data)
        return decoded_data.decode("utf-8", errors="ignore")
    except:
        raise ValueError("The card metadata is not encoded in base64.")

def parse_json(data: str):
    try:
        json_data = json.loads(data)
        return json_data
    except:
        raise ValueError("The card metadata is not encoded in JSON.")

def get_char(file_path: str):
    try:
        if file_path.endswith(".png"):
            data = read_metadata(file_path)
            if data == "":
                raise ValueError(f"The PNG file is not a card: {file_path}")
            decoded = parse_json(decode_base64(data))
            if "data" in decoded:
                return decoded["data"]
            else:
                return decoded
        if file_path.endswith(".json"):
            decoded =  parse_json(open(file_path, "r").read())
            if "data" in decoded:
                return decoded["data"]
            else:
                return decoded
    except:
        raise
    raise ValueError(f"The specified file type is not supported: {file_path}")