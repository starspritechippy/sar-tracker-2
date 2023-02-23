from io import StringIO

import discord
from discord.ext import commands

from helpers import read_items_names_prices
from image import image_from_url
from classes.bot import Bot


class CogOwner(commands.Cog):
    shop_text_template = """__**{shop_name}**__
{item1}: {price1} {currency}
{item2}: {price2} {currency}
{item3}: {price3} {currency}
{item4}: {price4} {currency}
{item5}: {price5} {currency}
{item6}: {price6} {currency}"""
    currencies = ("Carl Coins", "S.A.W. Tickets")
    shop_names = ("Cackling Carl's Cart", "S.A.W. Shop")

    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_check(self, ctx: discord.ApplicationContext):
        return await self.bot.is_owner(ctx.author)

    @commands.slash_command(
        name="testreal",
        description="test scenario for the real thing",
        guild_ids=[630988692693057566],
    )
    async def testreal(
        self,
        ctx: discord.ApplicationContext,
        carl: discord.Option(discord.Attachment, "Carl's Cart Image"),
        saw: discord.Option(discord.Attachment, "SAW Shop Image"),
    ):
        await ctx.defer()
        attachments = [carl, saw]

        text = StringIO()

        for idx, attachment in enumerate(attachments):
            image = image_from_url(attachment.url)
            items = read_items_names_prices(image)

            text.write(
                self.shop_text_template.format(
                    shop_name=self.shop_names[idx],
                    currency=self.currencies[idx],
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
        await ctx.send_followup(text.read())

    @commands.slash_command(
        name="debug",
        description="Set debug mode to either true or false",
        guild_ids=[630988692693057566],
    )
    @discord.option(
        "state",
        description="The value to set. `true` turns on debug features, `false` turns them off.",
        choices=["true", "false"],
    )
    async def toggle_debug(self, ctx: discord.ApplicationContext, state: str):
        if state == "true":
            self.bot.set_debug(True)
        else:
            self.bot.set_debug(False)
        await ctx.respond(f"Set debug mode to `{state}`!")


def setup(bot):
    bot.add_cog(CogOwner(bot))
