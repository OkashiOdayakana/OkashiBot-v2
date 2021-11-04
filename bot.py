import discord
from discord.commands.commands import Option, slash_command
import aiohttp
import json

with open("config.json") as config_f:
    config = json.load(config_f)

token = config["token"]
bot = discord.Bot()


async def retrieve_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return json.loads(await r.read())


@bot.slash_command(
    name="bible",
    description="Retrieve a verse from the bible",
)
async def bible(
    ctx,
    verse: Option(
        str,
        "The verse you wish to retrieve, random if none",
        required=False,
        default=None,
    ),
):
    if verse == None:
        verse = "random"

    bible_json = await retrieve_json(
        f"https://labs.bible.org/api/?passage={verse}&type=json"
    )
    book = bible_json[0]["bookname"]
    chapter = bible_json[0]["chapter"]
    verse_num = bible_json[0]["verse"]
    text = bible_json[0]["text"]
    embed = discord.Embed(title="The Holy Bible")
    embed.add_field(name=f"{book} {chapter}:{verse_num}", value=text)
    await ctx.respond(embed=embed)


bot.run(token)
