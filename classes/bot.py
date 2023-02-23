import logging

import discord
from discord import Bot


class CustomBot(Bot):

    def setup_logging(self):
        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("discord.log", mode="a", encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
        )
        logger.addHandler(handler)
        self.logger = logger
        self.logger.setLevel(logging.INFO)
        self.logger.info("Set up logger.")

    def set_debug(self, state: bool):
        if state:
            self.debug_state = True
            self.logger.setLevel(logging.DEBUG)
        else:
            self.debug_state = False
            self.logger.setLevel(logging.INFO)

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user}")

    async def on_message(self, message: discord.Message):
        if self.debug_state:
            self.logger.debug(
                "Received message. Author ID: {}, Author name: {}, Channel ID: {}, Channel name: {}, "
                "Attachments: {}, Content: {}".format(
                    message.author.id,
                    message.author,
                    message.channel.id,
                    message.channel,
                    len(message.attachments),
                    message.content,
                )
            )
