#Copyright Ghost Labs, Owner: ThatRealGhost#1811, Permission given.
import nextcord
from nextcord.ext import commands
from server_code import server_code

intents = nextcord.Intents.default()
intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix="g.", intents=intents)

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
                              
server_code()
bot.run('TOKEN_ID')
