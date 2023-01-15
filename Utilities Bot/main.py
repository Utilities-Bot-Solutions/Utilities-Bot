from discord import ChannelType
import nextcord
from nextcord.ext import commands
from server_code import server_code
import wavelink

intents = nextcord.Intents.default()
intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix="u.", intents=intents)

client = nextcord.Client(activity=nextcord.Game(name='Utilities Moderation Services'))

# or, for watching:
activity = nextcord.Activity(name='Utilities is active!', type=nextcord.ActivityType.watching)
client = nextcord.Client(activity=activity)

@bot.event
async def on_ready():
  print(f"{bot.user.name} is operational!")

logging = True
logschannel = 1053408045100711940

#Use the @bot.slash_command when making a new command

@bot.slash_command()
async def kick(interaction: nextcord.Interaction, user: nextcord.Member, reason: str):
  if not interaction.user.guild_permissions.kick_members:
    await interaction.response.send_message("You are not authorized to run this command.")
  else:
      await interaction.response.send_message(f"Kicked by {interaction.user.mention}")
      if logging is True:
        log_channel = bot.get_channel(logschannel)
        await log_channel.send(f"{user.mention} was kicked by {interaction.user.mention} for {reason}")
        await user.kick(reason=reason)

@bot.slash_command()
async def ban(interaction: nextcord.Interaction, user: nextcord.Member, reason: str):
    if not interaction.user.guild_permissions.ban_members:
       await interaction.response.send_message("You are not authorized to run this command")
    else:
      await interaction.response.send_message(f"Banned by {interaction.user.mention}")
      if logging is True:
        log_channel = bot.get_channel(logschannel)
        await log_channel.send(f"{user.mention} was banned by {interaction.user.mention} for {reason}")
        await user.ban(reason=reason)

@bot.slash_command()
async def unban(interaction: nextcord.Interaction, user: nextcord.User, reason: str):
  if not interaction.user.guild_permissions.ban_members:
    await interaction.response.send_message("You are not authorized to run this command.")
  else:
    await interaction.guild.unban(nextcord.Object(id=user.id), reason=reason)
    if logging is True:
       log_channel = bot.get_channel(logschannel)
       await log_channel.send(f"{user.mention} was unbanned by {interaction.user.mention} for {reason}")
       await int.unban(reason=reason)

@bot.slash_command()
async def timeout(interaction: nextcord.Interaction, user: nextcord.User, reason: str):
  if not interaction.user.guild_permissions.kick_members:
    await interaction.response.send_message("You are not authorized to run this command.")
  else:
      await interaction.guild.kick_members(nextcord.Object(id=user.id), reason=reason)
      if logging is True:
         log_channel = bot.get_channel(logschannel)
         await log_channel.send(f"{user.mention} was put in timeout by {interaction.user.mention} for {reason}")
         await user.timeout(reason=reason)

@bot.event
async def joined(ctx, *, member: nextcord.Member):
  await ctx.send(f'{member} joined on {member.joined_at}')

#Note: When using this command, don't abuse it.
@bot.slash_command()
async def test(ctx, arg):
  await ctx.send(arg)

@bot.event
async def on_wavelink_track_end(player:wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx
    vc : player = ctx.voice_client
    
    if vc.loop:
        return await vc.play(track)
    next_song= vc.queue.get()
    await vc.play(next_song)
    await ctx.send(f"Playing: {next_song.title}")
@bot.slash_command()
async def play(ctx: commands.Context,*, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not ctx.author.voice:
        return await ctx.send("Please join a VC.")
    elif not ctx.author.voice != ctx.me.voice:
        return await ctx.send("Please be in the same VC.")
    else:
        vc : wavelink.Player= ctx.voice_client
    if vc.queue.is_empty:
        await vc.play(search)
        await ctx.send(f"Playing: {search.title}")
    else:
        await vc.queue.put_wait(search)
        await ctx.send(f"Added {search.title} to the queue.")
    vc.ctx = ctx
    setattr(vc,"loop",False)
@bot.slash_command()
async def queue(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Please let me join a VC.")
    elif not ctx.author.voice:
        return await ctx.send("Please join a VC.")
    elif not ctx.author.voice != ctx.me.voice:
        return await ctx.send("Please be in the same VC.")
    else:
        vc: wavelink.Player = ctx.voice_client
    if vc.queue.is_empty:
        return await ctx.send("Queue is empty.")
                              
server_code()
bot.run('TOKEN_ID')
