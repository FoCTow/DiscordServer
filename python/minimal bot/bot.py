import discord

client = discord.Client()


x = {
  "content": "Hello, World!",
  "tts": False,
  "embed": {
    "title": "Hello, Embed!",
    "description": "This is an embedded message."
  }
}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('e! '):
        await message.channel.send('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE! <3')
        embed = discord.Embed( payload_json = x )
        await message.channel.send(embed=embed)



client.run('Nzc5MDI5ODI5MDcyMTkxNDg4.X7amEA.pfrXCkGNT5aDX6EW8BL9oaEG86c')