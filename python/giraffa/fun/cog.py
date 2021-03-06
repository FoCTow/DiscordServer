#----------------------------------------------------------------------------------------------------------
import discord
from discord.ext import commands
#----------------------------------------------------------------------------------------------------------
from . import ask
#----------------------------------------------------------------------------------------------------------
class Fun( commands.Cog ):
    #------------------------------------------------------------------------------------------------------
    def __init__(self, giraffa):
        self.giraffa = giraffa
    #------------------------------------------------------------------------------------------------------
    #@commands.Cog.listener()
    #async def on_ready(self):
    #    print('TEST')
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def ask(self, ctx, *, question=None):
        await ask.ask.cmd( ctx, question )
    #----------------------------------------------------------------------------------------------------------
    @commands.command()
    async def choose(self, ctx, *, options=None):
        await ask.ask.choose(ctx, options)
    #----------------------------------------------------------------------------------------------------------
    @commands.command()
    async def harro(self, ctx):
        await ctx.send('EEEEEEEEEEEEEEEEEEE! <3')
    #----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
def setup(giraffa):
    giraffa.add_cog(Fun(giraffa))
#----------------------------------------------------------------------------------------------------------