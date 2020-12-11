import discord
import aiohttp

client = discord.Client()

@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(msg):
    if msg.author != client.user:
        return
    elif msg.guild is None:
        return
    if msg.content == "!steal":
        try:
            id = int(msg.content[7:])
        except ValueError:
            return await msg.channel.send("Wrong ID!")

        guild = client.get_guild(id)
        if guild is None:
            return await msg.channel.send("Wrong ID!")
        
        defurl = "https://cdn.discordapp.com/emojis/"

        async def upload(name, id=None, url=defurl):
            async with aiohttp.ClientSession() as s:

                def URL():
                    if not id:
                        return url
                    else:
                        return url + id

                async with s.get(URL()) as r:
                    if r.status != 200:
                        return await msg.channel.send(
                            f"I can't upload the emoji's url\nStatus: {r.status}"
                        )
                    img = await r.read()
                    edit = await msg.channel.send("Creating...")
                    try:
                        await msg.guild.create_custom_emoji(name=name, image=img)
                    except discord.errors.HTTPException as e:
                        e = str(e).split(":")[-1]
                        embed = discord.Embed(title="Failed to create a new emoji", description=e)
                        return await msg.channel.send(embed=embed)
                    await edit.edit(content="Created new emoji!")

        for emo in guild.emojis:
            emoji = str(emo.url)
            name = emo.name

            await upload(name, url=emoji)
    

client.run('token', self_bot=True)
