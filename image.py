from PIL import Image
import base64
from io import BytesIO

buffered = BytesIO()

def merge_image(base, icon):
    file
    x_off = 0
    y_off = 0
    if icon == 0:
        png = "trumpr.png"
        x_off = 30
    elif icon == 1:
        png = "boldr.png"
        x_off = 200
    elif icon == 2:
        png = "42r.png"
        x_off = 200
        y_off = 200
    img = Image.open(BytesIO(base64.b64decode(base))).convert("RGBA")
    p = Image.open(png).convert("RGBA")
    x, y = p.size
    img.paste(p, (x_off, y_off, x + x_off, y+ y_off), p)
    #img.save("test.png", format="png")
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue())

with open ("test.txt", "r") as myfile:
    data=myfile.readlines()
merge_image(data[0], 2)
