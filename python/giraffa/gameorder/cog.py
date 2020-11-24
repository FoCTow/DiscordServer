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
        orderFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        rulesFILE = f'{dataDIR}\\{AT.FILE_RULES}'
        helpFILE = f'{dataDIR}\\{AT.FILE_HELP}'
        myorderFILE = f'{dataDIR}\\{AT.FILE_MYORDER}'
        #--------------------------------------------------------------------------------------------------
        startDATE = datetime.datetime.now().strftime("%d %m %Y")
        #--------------------------------------------------------------------------------------------------
        if not os.path.isfile(orderFILE):
            await self.writeJson( orderFILE, {"name":"","banner":"","closes":startDATE,"available":0,"games":[]})
            await ctx.send(AT.MSG_MASTER_CREATED)
            print(f'gameorder data template created: {orderFILE}')
        else: await ctx.send( AT.MSG_MASTER_EXISTS )
        #--------------------------------------------------------------------------------------------------
        if not os.path.isfile(rulesFILE):
            await self.writeJson( rulesFILE, {"embeds":[{"description":"This is an embed"}]})
            await ctx.send(AT.MSG_RULES_CREATED)
            print(f'gameorder rules template created: {orderFILE}')
        else: await ctx.send( AT.MSG_RULES_EXISTS )
        #--------------------------------------------------------------------------------------------------
        if not os.path.isfile(helpFILE):
            await self.writeJson( helpFILE, {"embeds":[{"description":"This is an embed"}]})
            await ctx.send(AT.MSG_HELP_CREATED)
            print(f'gameorder help template created: {orderFILE}')
        else: await ctx.send( AT.MSG_HELP_EXISTS )
        #--------------------------------------------------------------------------------------------------
        if not os.path.isfile(myorderFILE):
            await self.writeJson(myorderFILE, {"embeds":[{"description":"This is an embed"}]})
            await ctx.send(AT.MSG_MYORDER_CREATED)
            print(f'gameorder myorder template created: {orderFILE}')
        else:
            await ctx.send(AT.MSG_MYORDER_EXISTS)
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.has_permissions( administrator=True )
    async def gameorderdelete( self, ctx ):
        dataDIR = await self.getServerData( ctx )
        orderFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        rulesFILE = f'{dataDIR}\\{AT.FILE_RULES}'
        helpFILE = f'{dataDIR}\\{AT.FILE_HELP}'
        myorderFILE = f'{dataDIR}\\{AT.FILE_MYORDER}'
        #--------------------------------------------------------------------------------------------------
        if os.path.isfile(orderFILE):
            os.remove(orderFILE)
            await ctx.send(AT.MSG_MASTER_DELETED)
            print( f'gameorder data deleted: {orderFILE}' )
        #--------------------------------------------------------------------------------------------------
        if os.path.isfile(rulesFILE):
            os.remove(rulesFILE)
            await ctx.send(AT.MSG_RULES_DELETED)
            print( f'gameorder rules deleted: {rulesFILE}' )
        #--------------------------------------------------------------------------------------------------
        if os.path.isfile(helpFILE):
            os.remove(helpFILE)
            await ctx.send(AT.MSG_HELP_DELETED)
            print( f'gameorder help deleted: {helpFILE}' )
        #--------------------------------------------------------------------------------------------------
        if os.path.isfile(myorderFILE):
            os.remove(myorderFILE)
            await ctx.send(AT.MSG_MYORDER_DELETED)
            print(f'gameorder myorder deleted: {helpFILE}')
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.has_permissions( administrator=True )
    async def gameorderlist( self, ctx ):
        pass
    #------------------------------------------------------------------------------------------------------
    ##------------------------------------------------------------------------------------------------------
    @commands.command()
    async def test( self, ctx ):
        await ctx.author.send(AT.MSG_ORDER_ADD_SUCCESS.format("PSX - stell dir vor das sei ein spiel"))
        #await ctx.send( "<a:ab_a:780841271592747009>" )
        #await ctx.send( "<a:BanaNya:773671173627969576>" )
        #await ctx.send( "<a:ezgif42ee28b6f7860:772578058569252925>" )
    ##------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def orderlist(self, ctx):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        orderFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        if not await self.orderDataCheck(ctx, orderFILE): return
        #--------------------------------------------------------------------------------------------------
        with open( orderFILE, "r", encoding='utf-8' ) as infile: jsonDATA = json.load( infile )
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
        for i, string in enumerate(embeds):
            totalRemaining = int(jsonDATA["available"])
            if i == 0: string = AT.TXT_TOTAL_AVAILABLE.format(20-totalRemaining, totalRemaining) + string
            embed = discord.Embed.from_dict({"description":string, "color":3355443})
            await ctx.send( embed=embed )
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def myorder( self, ctx ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData(ctx)
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        userDATA = f'{dataDIR}\\orders\\{ctx.author.id}.json'
        myorderFILE = f'{dataDIR}\\{AT.FILE_MYORDER}'
        #--------------------------------------------------------------------------------------------------
        if not await self.orderDataCheck(ctx, dataFILE): return
        if not await self.userDataCheck(ctx, userDATA): return
        if not await self.hasOrderedCheck(ctx, userDATA): return
        #--------------------------------------------------------------------------------------------------
        with open(dataFILE, "r", encoding='utf-8') as infile: orderJSON = json.load(infile)
        with open(userDATA) as infile: userJSON = json.load(infile)
        with open(myorderFILE, "r", encoding='utf-8') as infile: myorderJSON = json.load(infile)
        #--------------------------------------------------------------------------------------------------
        embed = myorderJSON["embeds"][0]
        myGameIDS = [int(x) for x in userJSON["games"]]
        priceTotal = 0
        #--------------------------------------------------------------------------------------------------
        embed["description"] += "\n\n"
        #--------------------------------------------------------------------------------------------------
        for id in myGameIDS:
            name = orderJSON["games"][id]["name"]
            price = float(orderJSON["games"][id]["price"])
            priceTotal += price
            embed["description"] += f'`{(10>id)*" "}{id} | {name}{(48-len(name))*" "}{(10>price)*" "}{price}0 €`\n'
        #--------------------------------------------------------------------------------------------------
        embed["description"] += f'\n`price total{42*" "}{(10>priceTotal)*" "}{priceTotal}0 €`\n'
        #--------------------------------------------------------------------------------------------------
        post = discord.Embed.from_dict(embed)
        await ctx.send(embed=post)
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def orderinfo( self, ctx ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        orderFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        rulesFILE = f'{dataDIR}\\{AT.FILE_RULES}'
        #--------------------------------------------------------------------------------------------------
        if not await self.orderDataCheck(ctx, orderFILE): return
        #--------------------------------------------------------------------------------------------------
        with open( rulesFILE, "r", encoding='utf-8' ) as infile: jsonDATA = json.load( infile )
        #--------------------------------------------------------------------------------------------------
        for embedDATA in jsonDATA["embeds"]:
            embed = discord.Embed.from_dict(embedDATA)
            await ctx.send( embed=embed )
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def ordercmds( self, ctx ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        helpFILE = f'{dataDIR}\\{AT.FILE_HELP}'
        #--------------------------------------------------------------------------------------------------
        if not await self.orderDataCheck(ctx, dataFILE): return
        #--------------------------------------------------------------------------------------------------
        with open( helpFILE, "r", encoding='utf-8' ) as infile: jsonDATA = json.load( infile )
        #--------------------------------------------------------------------------------------------------
        for embedDATA in jsonDATA["embeds"]:
            embed = discord.Embed.from_dict( embedDATA )
            await ctx.send( embed=embed )
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def orderagree( self, ctx ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData(ctx)
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        userDATA = f'{dataDIR}\\orders\\{ctx.author.id}.json'
        #--------------------------------------------------------------------------------------------------
        if not await self.orderDataCheck(ctx, dataFILE): return
        await self.userDataCheck(ctx, userDATA, forcePass=True)
        #--------------------------------------------------------------------------------------------------
        with open( userDATA ) as infile: userJSON = json.load( infile )
        userJSON["agreed"] = True
        await self.writeJson( userDATA, userJSON )
        await ctx.author.send(AT.MSG_ORDER_AGREED.format(ctx.author.name))
        print(f'user {ctx.author.name} agreed to order rules')
        #--------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def orderadd( self, ctx, gameID ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        userDATA = f'{dataDIR}\\orders\\{ctx.author.id}.json'
        #--------------------------------------------------------------------------------------------------
        if not await self.orderDataCheck(ctx, dataFILE): return
        if not await self.orderOpenCheck(ctx, dataFILE): return
        if not await self.userDataCheck(ctx, userDATA): return
        if not await self.canOrderAddCheck(ctx, dataFILE, gameID): return
        #--------------------------------------------------------------------------------------------------
        with open(dataFILE, "r", encoding='utf-8') as infile: orderJSON = json.load( infile )
        availableID = orderJSON["games"][int(gameID)]["availableID"]
        #--------------------------------------------------------------------------------------------------
        for game in orderJSON["games"]:
            if game["availableID"] == availableID: game["available"] -= 1
        #--------------------------------------------------------------------------------------------------
        orderJSON["available"] -= 1
        await self.writeJson( dataFILE, orderJSON )
        #--------------------------------------------------------------------------------------------------
        with open(userDATA) as infile: userJSON = json.load(infile)
        userJSON["games"].append(int(gameID))
        await self.writeJson( userDATA, userJSON )
        #--------------------------------------------------------------------------------------------------
        await ctx.author.send(AT.MSG_ORDER_ADD_SUCCESS.format(orderJSON["games"][int(gameID)]["name"]))
    #------------------------------------------------------------------------------------------------------
    @commands.command()
    async def orderremove( self, ctx, gameID ):
        #--------------------------------------------------------------------------------------------------
        dataDIR = await self.getServerData( ctx )
        dataFILE = f'{dataDIR}\\{AT.FILE_ORDER}'
        userDATA = f'{dataDIR}\\orders\\{ctx.author.id}.json'
        #--------------------------------------------------------------------------------------------------
        if not await self.orderDataCheck(ctx, dataFILE): return
        if not await self.orderOpenCheck(ctx, dataFILE): return
        if not await self.userDataCheck(ctx, userDATA): return
        if not await self.canOrderRemoveCheck(ctx, userDATA, gameID): return
        #--------------------------------------------------------------------------------------------------
        with open( dataFILE, "r", encoding='utf-8' ) as infile: orderJSON = json.load( infile )
        availableID = orderJSON["games"][int(gameID)]["availableID"]
        #--------------------------------------------------------------------------------------------------
        for game in orderJSON["games"]:
            if game["availableID"] == availableID: game["available"] += 1
        #--------------------------------------------------------------------------------------------------
        orderJSON["available"] += 1
        await self.writeJson( dataFILE, orderJSON )
        #--------------------------------------------------------------------------------------------------
        with open(userDATA) as infile: userJSON = json.load(infile)
        userJSON["games"].remove(int(gameID))
        await self.writeJson(userDATA, userJSON)
        #--------------------------------------------------------------------------------------------------
        await ctx.author.send(AT.MSG_ORDER_REMOVE_SUCCESS.format(orderJSON["games"][int(gameID)]["name"]))
    #------------------------------------------------------------------------------------------------------
    async def getServerData( self, ctx ):
        return f'{self.dataRoot}\\{ctx.message.guild.id}\\gameorder'
    #------------------------------------------------------------------------------------------------------
    @staticmethod
    async def writeJson( file, jsonDict ):
        fileDIR = os.path.dirname(file)
        if not os.path.exists( fileDIR ): os.makedirs( fileDIR )
        with open(file, "w+") as outfile: json.dump(jsonDict, outfile, indent=4, sort_keys=True)
    #------------------------------------------------------------------------------------------------------
    @staticmethod
    async def orderDataCheck( ctx, dataFILE ):
        #--------------------------------------------------------------------------------------------------
        if os.path.isfile(dataFILE):
            with open(dataFILE) as infile: orderDATA = json.load(infile)
            if orderDATA["name"] and orderDATA["games"]: return True
        #--------------------------------------------------------------------------------------------------
        await ctx.send(AT.ORDER_VAILD_ERROR, delete_after=3)
        return False
    #------------------------------------------------------------------------------------------------------
    @staticmethod
    async def orderOpenCheck( ctx, dataFILE ):
        #--------------------------------------------------------------------------------------------------
        with open(dataFILE) as infile: orderDATA = json.load(infile)
        d,m,y = [int(x) for x in orderDATA["closes"].split(" ")]
        if datetime.datetime(y,m,d) >= datetime.datetime.now(): return True
        #--------------------------------------------------------------------------------------------------
        await ctx.send(AT.ORDER_DATE_ERROR, delete_after=3)
        return False
    #------------------------------------------------------------------------------------------------------
    async def userDataCheck( self, ctx, dataFILE, forcePass=False ):
        #--------------------------------------------------------------------------------------------------
        if not os.path.isfile(dataFILE):
            await self.writeJson( dataFILE, {"username":ctx.author.name,"displayname":ctx.author.display_name,"userid":ctx.author.id,"agreed":False,"paid":False,"games":[]})
            print(f'user data template created for {ctx.author.name}: {dataFILE}')
        #--------------------------------------------------------------------------------------------------
        with open( dataFILE ) as infile: userDATA = json.load( infile )
        if not forcePass and not userDATA["agreed"]:
            await ctx.send(AT.ORDER_AGREED_ERROR, delete_after=5)
            return False
        #--------------------------------------------------------------------------------------------------
        return True
    #------------------------------------------------------------------------------------------------------
    @staticmethod
    async def canOrderAddCheck( ctx, dataFILE, gameID ):
        #--------------------------------------------------------------------------------------------------
        try: targetID = int(gameID)
        except ValueError:
            await ctx.send(AT.INDEX_TYPE_ERROR.format(gameID), delete_after=3)
            return False
        #--------------------------------------------------------------------------------------------------
        if os.path.isfile( dataFILE ):
            #----------------------------------------------------------------------------------------------
            with open( dataFILE ) as infile: orderDATA = json.load( infile )
            if targetID<0 or targetID>=len(orderDATA["games"]):
                await ctx.send(AT.INDEX_RANGE_ERROR.format(gameID), delete_after=3)
                return False
            #----------------------------------------------------------------------------------------------
            if orderDATA["games"][targetID]["available"] < 1:
                await ctx.send(AT.ORDER_AVAILABLE_ERROR, delete_after=3)
                return False
            #----------------------------------------------------------------------------------------------
            if  orderDATA["available"] < 1:
                await ctx.send(AT.ORDER_TOTAL_AVAILABLE_ERROR, delete_after=3)
                return False
            #----------------------------------------------------------------------------------------------
        return True
    #------------------------------------------------------------------------------------------------------
    @staticmethod
    async def canOrderRemoveCheck( ctx, dataFILE, gameID ):
        #--------------------------------------------------------------------------------------------------
        try: targetID = int(gameID)
        except ValueError:
            await ctx.send(AT.INDEX_TYPE_ERROR.format(gameID), delete_after=3)
            return False
        #--------------------------------------------------------------------------------------------------
        if os.path.isfile( dataFILE ):
            #----------------------------------------------------------------------------------------------
            with open(dataFILE) as infile: userDATA = json.load(infile)
            if not targetID in userDATA["games"]:
                await ctx.send(AT.ORDER_REMOVE_ERROR.format(targetID), delete_after=3)
                return False
        #--------------------------------------------------------------------------------------------------
        return True
    #------------------------------------------------------------------------------------------------------
    @staticmethod
    async def hasOrderedCheck( ctx, dataFILE ):
        #--------------------------------------------------------------------------------------------------
        if os.path.isfile( dataFILE ):
            #----------------------------------------------------------------------------------------------
            with open(dataFILE) as infile: userDATA = json.load(infile)
            if not userDATA["games"]:
                await ctx.send(AT.ORDER_MYORDER_ERROR, delete_after=3)
                return False
        #--------------------------------------------------------------------------------------------------
        return True
    #------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
def setup(giraffa):
    giraffa.add_cog(Gameorder(giraffa))
#----------------------------------------------------------------------------------------------------------