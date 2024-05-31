import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
GUILD_ID = os.environ['Token']
ROLE_ID = os.environ['R']
LOG_CHANNEL_ID = os.environ['L']
VERIFICATION_CHANNEL_ID = os.environ['V']

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

code_check_url = "http://localhost:5000/check-code/"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.channel.id == VERIFICATION_CHANNEL_ID:
        code = message.content.strip()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{code_check_url}{code}") as resp:
                data = await resp.json()
                if data['valid']:
                    role = discord.utils.get(message.guild.roles, id=ROLE_ID)
                    await message.author.add_roles(role)
                    log_channel = bot.get_channel(LOG_CHANNEL_ID)
                    await log_channel.send(f'{message.author} has been given the temporary role.')
                    
                    # Schedule role removal after 1 hour
                    await asyncio.sleep(3600)
                    await message.author.remove_roles(role)
                    await log_channel.send(f'{message.author}\'s temporary role has expired.')

bot.run(os.environ['Token'])
