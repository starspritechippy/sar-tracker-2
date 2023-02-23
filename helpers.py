import os
import string

from discord import Message
from PIL import Image

from image import get_item_names_prices, preprocess_image, read_text
from regex import price_finder_pattern, timestamp_pattern


def from_sar_server_check(message: Message) -> bool:
    if (
        message.channel.id != int(os.getenv("SAR_CHANNEL_ID"))
        or
        # message.author.id != int(os.getenv("SAR_AUTHOR_ID")) or
        not timestamp_pattern.match(message.content)
        or len(message.attachments) != 2
    ):
        return False
    return True


def read_items_names_prices(image: Image.Image) -> list[tuple[str, int]]:
    items = get_item_names_prices(image)
    items_text = []
    for idx in range(6):
        prepared_name = preprocess_image(items["names"][idx])
        name_text = read_text(prepared_name).strip()

        price_text = read_text(items["prices"][idx]).strip()
        price = price_finder_pattern.search(price_text).group(1)

        items_text.append((string.capwords(name_text), int(price)))

    return items_text
