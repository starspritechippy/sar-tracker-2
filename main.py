import os
from io import StringIO
from sys import platform

import discord
from classes import CustomBot
import pytesseract
from dotenv import load_dotenv

from helpers import from_sar_server_check, read_items_names_prices
from image import image_from_url


def main():
    load_dotenv()
    if platform == "win32":
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Users\maxhe\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        )

    shop_text_template = """__**{shop_name}**__
    {item1}: {price1} {currency}
    {item2}: {price2} {currency}
    {item3}: {price3} {currency}
    {item4}: {price4} {currency}
    {item5}: {price5} {currency}
    {item6}: {price6} {currency}"""
    currencies = ("Carl Coins", "S.A.W. Tickets")
    shop_names = ("Cackling Carl's Cart", "S.A.W. Shop")

    bot = CustomBot()
    bot.setup_logging()

    @bot.event
    async def on_ready():
        bot.logger.info(f"Logged in as {bot.user}")

    @bot.event
    async def on_message(message: discord.Message):
        if not from_sar_server_check(message):
            return

        text = StringIO()

        for idx, attachment in enumerate(message.attachments):
            image = image_from_url(attachment.url)
            items = read_items_names_prices(image)

            text.write(
                shop_text_template.format(
                    shop_name=shop_names[idx],
                    currency=currencies[idx],
                    item1=items[0][0],
                    price1=items[0][1],
                    item2=items[1][0],
                    price2=items[1][1],
                    item3=items[2][0],
                    price3=items[2][1],
                    item4=items[3][0],
                    price4=items[3][1],
                    item5=items[4][0],
                    price5=items[4][1],
                    item6=items[5][0],
                    price6=items[5][1],
                )
            )

            if idx == 0:
                text.write("\n\n---------\n\n")

        text.seek(0)
        await message.channel.send(text.read())

    bot.load_extension("cogs.owner")

    token = str(os.getenv("DISCORD_TOKEN"))

    bot.run(token)
    return


if __name__ == "__main__":
    main()
