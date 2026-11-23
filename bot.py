


import os, json, random, aiohttp, discord
from discord import app_commands

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN") or "MTU3NDM1MzU2NzA4OTY5Njc4OA.GiFSOw.G6HUSX9tVShVLUqGOpJV2yZzp5o9xrHyi5i1-4"
GIPHY_KEY = os.environ.get("GIPHY_KEY") or "b7CMlaVahXFekiU6yCohEW5AqAzqfYow"

GIFS = json.load(open("gifs.json"))
client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

async def giphy(query):
async with aiohttp.ClientSession() as s:
async with s.get(
"https://api.giphy.com/v1/gifs/search",
params={"api_key": GIPHY_KEY, "q": query,
"limit": 10, "rating": "pg-13"},
) as r:
data = (await r.json())["data"]
return random.choice(data)["url"] if data else None

@tree.command(name="summon", description="Summon a GIF")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def summon(interaction: discord.Interaction, query: str):
await interaction.response.defer()
words = query.lower().split()
hits = [u for k, u in GIFS.items()
if all(w in k.lower() for w in words)]
url = random.choice(hits) if hits else await giphy(query)
await interaction.followup.send(url or "No gif found 😔")

@summon.autocomplete("query")
async def suggest(interaction: discord.Interaction, current: str):
return [app_commands.Choice(name=k, value=k)
for k in GIFS if current.lower() in k.lower()][:25]

@client.event
async def on_ready():
await tree.sync()

client.run(DISCORD_TOKEN)
