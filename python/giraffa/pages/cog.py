#----------------------------------------------------------------------------------------------------------
import discord
from discord.ext import commands
#----------------------------------------------------------------------------------------------------------
class Pages( commands.Cog ):
    #------------------------------------------------------------------------------------------------------
    def __init__(self, giraffa):
        self.giraffa = giraffa
    #------------------------------------------------------------------------------------------------------
    #@commands.Cog.listener()
    #async def on_ready(self):
    #    print('TEST')
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def pages( self, ctx ):
        print( 'test' )
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def pagelist(self, ctx):
        print('COG')
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def pagenew( self, ctx ):
        print( 'COG' )
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def pakeedit( self, ctx ):
        print( 'COG' )
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def pagemove( self, ctx ):
        print( 'COG' )
    #------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
def setup(giraffa):
    giraffa.add_cog(Pages(giraffa))
#----------------------------------------------------------------------------------------------------------