#----------------------------------------------------------------------------------------------------------
import discord
import os
from discord.ext import commands
#----------------------------------------------------------------------------------------------------------
from secret import secrets
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
giraffa = commands.Bot( command_prefix=['e! ', 'e!',  'giraffa ', 'giraffa'] )
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
# >>> MODULE HANDLING
#----------------------------------------------------------------------------------------------------------
@giraffa.command()
@commands.has_permissions(administrator=True)
async def load(ctx, moduleName):
    giraffa.load_extension(f'{moduleName}.cog')
#----------------------------------------------------------------------------------------------------------
@giraffa.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, moduleName):
    giraffa.unload_extension(f'{moduleName}.cog')
#----------------------------------------------------------------------------------------------------------
@giraffa.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, moduleName=None):
    if moduleName: giraffa.reload_extension(f'{moduleName}.cog')
    else:
        for module in list(giraffa.extensions): giraffa.reload_extension(f'{module}')
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
@giraffa.command()
@commands.has_permissions(administrator=True)
async def run(ctx, *, cmd):
    exec(cmd)
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
# >>> ERROR HANDLING
#----------------------------------------------------------------------------------------------------------
@giraffa.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(":warning:  EEEEEEEEE? - It appears you are missing permission to run this command")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":grey_exclamation:  BLLEEGG... - It appears this command was missing arguments")
    else: raise error
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
# >>> EVENT EXAMPLES
#----------------------------------------------------------------------------------------------------------
@giraffa.event
async def on_ready():
    print('We have logged in as {0.user}'.format( giraffa ) )
#----------------------------------------------------------------------------------------------------------
@giraffa.event
async def  on_member_join(member):
    print('{} has joined the server'.format(member))
#----------------------------------------------------------------------------------------------------------
@giraffa.event
async def  on_member_remove(member):
    print('{} has left the server'.format(member))
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
# >>> STARTUP
#----------------------------------------------------------------------------------------------------------
for subDir in next(os.walk('.'))[1]:
    if os.path.isfile(f'./{subDir}/cog.py'):
        giraffa.load_extension( f'{subDir}.cog' )
#----------------------------------------------------------------------------------------------------------
giraffa.run(secrets.BOT_TOKEN)
#----------------------------------------------------------------------------------------------------------