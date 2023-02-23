from io import BytesIO

import httpx
import pytesseract
from PIL import Image, ImageFilter

from constants import name_locations, price_locations


def image_from_url(url: str) -> Image.Image:
    # TODO validate url
    with httpx.Client() as client:
        response = client.get(url)

    if response.status_code != 200:
        raise Exception  # FIXME absolutely need to define a custom error

    image_bytes = BytesIO(response.read())

    return Image.open(image_bytes)


def get_item_names_prices(image: Image.Image):
    items = {"names": [], "prices": []}
    for idx, location in enumerate(name_locations):
        crop = image.crop(location.to_tuple())
        items["names"].append(crop)
        # crop.save(f"output/names/{idx}.png")

    for idx, location in enumerate(price_locations):
        crop = image.crop(location.to_tuple())
        items["prices"].append(crop)
        # crop.save(f"output/prices/{idx}.png")

    return items


def image_threshold(img: Image.Image, threshold: int) -> Image.Image:
    img = img.convert("L")

    return img.point(lambda p: p > threshold and 255)


def preprocess_image(img: Image.Image) -> Image.Image:
    img_threshold = image_threshold(img, 190)
    img_blur = img_threshold.filter(ImageFilter.BoxBlur(0.1))

    return img_blur


def read_text(img: Image.Image) -> str:
    """this assumes the given image is already preprocessed"""
    return pytesseract.image_to_string(img, config="--psm 6")
