import asyncio
import discord
from discord.ext import commands
from apibay import ApiBay, Category
from torrent import PyTorrent

bot = commands.Bot(command_prefix='!')  # Create a bot instance
ab = ApiBay()  # Create a ApiBay instance
qb = PyTorrent(category="Turkflix")  # Create a PyTorrent instance

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')  # Print bot's username when it's ready

@bot.command()
async def search(ctx, *args):
    """Search for a movie on The Pirate Bay."""
    message = " ".join(args)

    results = ab.search(message, results_count=3, category=Category.VIDEO)  # Search for the movie using TPB package

    if results:
        # Display the search results
        for index, result in enumerate(results, start=1):
            embed = discord.Embed(title=f"{index}. **{result.name}**", color=discord.Color.blue())
            embed.add_field(name="Size", value=f"{round(int(result.size) / 1073741824, ndigits=2)}gb", inline=True)
            embed.add_field(name="Seeders", value=f"{result.seeders}", inline=True)
            embed.add_field(name="ID", value=f"{result.id}", inline=True)
            if result.imdb != "":
                embed.add_field(name="IMDB", value=f"https://www.imdb.com/title/{result.imdb}/", inline=True)
            embed.set_footer(text=result.info_hash)

            message = await ctx.send(embed=embed)
            await message.add_reaction("📥")
        await ctx.send(embed=discord.Embed(title=f"Add to Turkflix by reacting with 📥", color=discord.Color.blurple()))

@bot.command()
async def status(ctx, *args):
    """Check progress of torrent downloads."""
    # message = " ".join(args)
    status = qb.status(results_count=3)

    if len(status) == 0:
        await ctx.send(embed=discord.Embed(title="No active downloads", color=discord.Color.green()))
    
    for index, torrent in enumerate(status, start=1):
        color = discord.Color.gold() if torrent.progress < 100 else discord.Color.green()
        embed = discord.Embed(title=f"{index}. **{torrent.name}**", color=color)
        embed.add_field(name="Status", value=f"{torrent.progress}% Complete", inline=True)
        await ctx.send(embed=embed)

@bot.event
async def on_reaction_add(reaction, member):
    """Download the movie when the user reacts with 📥."""
    async def send_embed(reaction, embed):
        guild = reaction.message.guild
        channel = discord.utils.get(guild.text_channels, name='general')
        if channel is not None:
            return await channel.send(embed=embed)

    if str(reaction.emoji) == "📥" and not member.bot:
        # Replace this with the code to download the movie
        qb.download(reaction.message.embeds[0].footer.text)
        embed = discord.Embed(title=f"Downloading {reaction.message.embeds[0].title} has started! 🎬", color=discord.Color.green())
        embed.set_footer(text=reaction.message.embeds[0].footer.text)

        message = await send_embed(reaction, embed)
        await message.add_reaction("❌")

    elif str(reaction.emoji) == "❌" and not member.bot:
        # Replace this with the code to download the movie
        await reaction.message.delete()
        qb.cancel(reaction.message.embeds[0].footer.text)
        embed = discord.Embed(title=f"Canceled {reaction.message.embeds[0].title} ❌", color=discord.Color.red())
        
        message = await send_embed(reaction, embed)


TOKEN = "YOUR_BOT_TOKEN"

bot.run(TOKEN)
