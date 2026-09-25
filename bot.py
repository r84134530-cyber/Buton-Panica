import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands

# --- Server web simplu cu Flask (pentru a ține Render mulțumit gratuit) ---
app = Flask('')

@app.route('/')
def home():
    return "Botul este online!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- Botul de Discord ---
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

DISPATCH_CHANNEL_ID = int(os.getenv("DISPATCH_CHANNEL_ID", "123456789012345678"))
ROLE_TO_PING_ID = int(os.getenv("ROLE_TO_PING_ID", "987654321098765432"))

@bot.command(name="panica")
async def panica(ctx, *, locatie: str = "Locație nespecificată"):
    try:
        await ctx.message.delete()
    except:
        pass

    channel = bot.get_channel(DISPATCH_CHANNEL_ID)
    if not channel:
        await ctx.send("Canalul de dispecerat nu a fost găsit!", ephemeral=True)
        return

    role_to_ping = ctx.guild.get_role(ROLE_TO_PING_ID)
    ping_mention = role_to_ping.mention if role_to_ping else "@here"

    embed = discord.Embed(
        title="🚨 COD ROȘU - BUTON DE PANICĂ 🚨",
        description="Un agent/membru a acționat butonul de panică și are nevoie de suport urgent!",
        color=discord.Color.red()
    )
    
    embed.add_field(name="👤 Solicitant:", value=ctx.author.mention, inline=True)
    embed.add_field(name="📍 Locație:", value=locatie, inline=True)
    embed.add_field(name="⏰ Status:", value="Echipajele sunt așteptate la fața locului!", inline=False)
    
    embed.set_footer(text="Sistem Dispecerat Automat • Roleplay")

    await channel.send(content=f"🚨 ATENȚIE {ping_mention}, intervenție necesară!", embed=embed)
    await ctx.author.send(f"⚠️ Ai declanșat butonul de panică! Dispeceratul a fost alertat la locația: **{locatie}**.")

@bot.event
async def on_ready():
    print(f"Botul de Dispecerat {bot.user} este online!")

# Pornește serverul web în fundal, apoi pornește botul
if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("TOKEN"))
    
