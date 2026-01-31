# images.py
from __future__ import annotations
import io
from flask import Blueprint, send_file
from db import q_one

images_bp = Blueprint("images", __name__)

def _image_mime(data:bytes)->str:
    if not data: return "image/png"
    sig = data[:12]
    if sig.startswith(b"\xff\xd8"): return "image/jpeg"
    if sig.startswith(b"\x89PNG\r\n\x1a\n"): return "image/png"
    if sig[:4] in (b"RIFF",) and sig[8:12] == b"WEBP": return "image/webp"
    if sig[:3] in (b"GIF",): return "image/gif"
    return "application/octet-stream"

# 1x1 transparent PNG
PLACEHOLDER_PNG = bytes.fromhex(
    "89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C4890000000A49444154789C6360000002000154A24F650000000049454E44AE426082"
)

@images_bp.route("/photo/box/<int:box_id>")
def photo_box(box_id:int):
    row = q_one("SELECT photo FROM boxes WHERE box_id=?", (box_id,))
    data = row["photo"] if row and row["photo"] is not None else None
    if not data:
        return send_file(io.BytesIO(PLACEHOLDER_PNG), mimetype="image/png")
    return send_file(io.BytesIO(data), mimetype=_image_mime(data))

@images_bp.route("/photo/item/<int:item_id>")
def photo_item(item_id:int):
    row = q_one("SELECT photo FROM items WHERE item_id=?", (item_id,))
    data = row["photo"] if row and row["photo"] is not None else None
    if not data:
        return send_file(io.BytesIO(PLACEHOLDER_PNG), mimetype="image/png")
    return send_file(io.BytesIO(data), mimetype=_image_mime(data))
