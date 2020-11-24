#----------------------------------------------------------------------------------------------------------
import discord
import json
import os
import datetime
from discord.ext import commands
#----------------------------------------------------------------------------------------------------------
from .attributes import attributes as AT
#----------------------------------------------------------------------------------------------------------
class Gameorder( commands.Cog ):
    #------------------------------------------------------------------------------------------------------
    def __init__(self, giraffa):
        self.giraffa = giraffa
        self.dataRoot = f'{os.path.dirname( __file__ ).split( "python" )[0]}data'
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.has_permissions( administrator=True )
    async def gameordercreate( self, ctx ):
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        #--------------------------------------------------------------------------------------------------
        startDATE = datetime.datetime.now().strftime("%d %m %Y")
        #--------------------------------------------------------------------------------------------------
        if not os.path.isfile(dataFILE):
            await self.writeJson( dataFILE, {"name":"","banner":"","closes":startDATE,"available":0,"games":[]})
            await ctx.send(AT.MSG_MASTER_CREATED)
            print(f'gameorder data template created: {dataFILE}')
        else: await ctx.send(AT.MSG_MASTER_EXISTS)
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.has_permissions( administrator=True )
    async def gameorderdelete( self, ctx ):
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        if os.path.isfile(dataFILE):
            os.remove(dataFILE)
            await ctx.send(AT.MSG_MASTER_DELETED)
            print( f'gameorder data deleted: {dataFILE}' )
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.has_permissions( administrator=True )
    async def orderlist( self, ctx ):
        pass
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def test( self, ctx ):
        #await ctx.send(AT.TEST)
        x = {
            "content": "Hello, World!",

            #"tts": False,
            "embed": {
                "color": 3355443,
                "title": "Hello, Embed!",
                "image": { "url": "https://github.com/FoCTow/DiscordServer/blob/master/assets/banners/christmas/Banner_Game_Order.png?raw=true", "width":.5 },
                "description": "This is an embedded message."
            }
        }

        embeds = [
            {
                "color": 3355443,
                "image": {"url": "https://github.com/FoCTow/DiscordServer/blob/master/assets/banners/christmas/Banner_Game_Order.png?raw=true"},
            },
            {
                "color": 3355443,
                "image": {"url": ""},
            },
        ]
        embed = discord.Embed.from_dict(x["embed"])
        await ctx.send( embed=embed )
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def order(self, ctx):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        if not await self.orderValidCheck( ctx, dataFILE, checkDATE=False ): return
        #--------------------------------------------------------------------------------------------------
        with open( dataFILE, "r", encoding='utf-8' ) as infile: jsonDATA = json.load( infile )
        #--------------------------------------------------------------------------------------------------
        embeds = []
        platform = None
        #--------------------------------------------------------------------------------------------------
        for i, game in enumerate(jsonDATA["games"]):
            #----------------------------------------------------------------------------------------------
            name = game["name"]
            price = float(game["price"])
            number = game["available"]
            unavailable = game["available"]<1 or jsonDATA["available"]<1
            #----------------------------------------------------------------------------------------------
            if not platform or not name.startswith(platform):
                platform = name.split("-")[0][:-1]
                embeds.append("")
            #----------------------------------------------------------------------------------------------
            embeds[-1] += f'{unavailable*"~~"}`{(10>i)*" "}{i} | {number}x {name}{(58-len(name))*" "}{(10>price)*" "}{price}0 €`{unavailable*"~~"}\n'
        #--------------------------------------------------------------------------------------------------
        for string in embeds:
            embed = discord.Embed.from_dict( {"description":string, "color": 3355443} )
            await ctx.send( embed=embed )
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def orderinfo( self, ctx ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        if not await self.orderValidCheck( ctx, dataFILE, checkDATE=False ): return
        #--------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def orderadd( self, ctx ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        if not await self.orderValidCheck(ctx, dataFILE ): return
        #--------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def orderremove( self, ctx ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        if not await self.orderValidCheck( ctx, dataFILE ): return
        #--------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def myorder( self, ctx ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        if not await self.orderValidCheck( ctx, dataFILE, checkDATE=False ): return
        #--------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    async def getServerData( self, ctx ):
        return f'{self.dataRoot}\\{ctx.message.guild.id}\\gameorder'
    #------------------------------------------------------------------------------------------------------
    async def writeJson( self, file, jsonDict ):
        fileDIR = os.path.dirname(file)
        if not os.path.exists( fileDIR ): os.makedirs( fileDIR )
        with open(file, "w+") as outfile: json.dump(jsonDict, outfile, indent=4, sort_keys=True)
    #------------------------------------------------------------------------------------------------------
    #async def loadJson( self, file ):
    #    with open( file, "r" ) as infile: return json.load( infile )
    #------------------------------------------------------------------------------------------------------
    async def orderValidCheck( self, ctx, dataFILE, checkDATE=True ):
        #--------------------------------------------------------------------------------------------------
        testPassed = False
        #--------------------------------------------------------------------------------------------------
        if os.path.isfile(dataFILE):
            with open(dataFILE) as infile: orderDATA = json.load(infile)
            if orderDATA["name"] and orderDATA["games"]: testPassed = True
        #--------------------------------------------------------------------------------------------------
        if not testPassed and not checkDATE:
            await ctx.send('EE!? Sorry, there seem to be no open Game Orders at this time')
            return False
        #--------------------------------------------------------------------------------------------------
        elif checkDATE:
            testPassed = False
            d,m,y = [int(x) for x in orderDATA["closes"].split(" ")]
            if datetime.datetime(y,m,d) >= datetime.datetime.now(): testPassed = True
        #--------------------------------------------------------------------------------------------------
        if not testPassed:
            await ctx.send('BLEGG... Sorry orders for this Game Order are no longer open')
            return False
        #--------------------------------------------------------------------------------------------------
        return True
    #------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
def setup(giraffa):
    giraffa.add_cog(Gameorder(giraffa))
#----------------------------------------------------------------------------------------------------------