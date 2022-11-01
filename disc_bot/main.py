import discord
from discord.ext import commands
import sqlite3
import datetime
import time
import os
from googletrans import Translator #Version: googletrans==3.1.0a0
# from discord_buttons_plugin import *

token = ''

bot = commands.Bot(command_pimport discord
from discord.ext import commands
import sqlite3
import datetime
import time
import os
from googletrans import Translator #Version: googletrans==3.1.0a0
# from discord_buttons_plugin import *

token = ''

bot = commands.Bot(command_prefix="?!", intents=discord.Intents.all())

bot.remove_command('help')

agma_id = 356145230342389760

db = sqlite3.connect('modmail.db')
cursor = db.cursor()

# Remove after running once
# cursor.execute("""
#     CREATE TABLE modmail (
#         user_id int,
#         channel_id int
#      )
# """)


def check(key):
    if key is None:
        return False
    else:
        return True


bot.user_id = None


@bot.event
async def on_ready():

    # agma, forums, b_forums = status()

    # channel = bot.get_channel(512586535011483648)  # the message's channel

    # msg_id1 = 971028738772971520
    # msg_id2 = 971028739490205777
    # msg_id3 = 973900585357156373

    # if agma != 200:
    #     agma = "❌"
    # elif agma == 200:
    #     agma = "✅"

    # if b_forums != 200:
    #     b_forums = "❌"
    # elif b_forums == 200:
    #     b_forums = "✅"

    # if forums != 200:
    #     forums = "❌"
    # elif forums == 200:
    #     forums = "✅"

    # msg1 = await channel.fetch_message(msg_id1)
    # msg2 = await channel.fetch_message(msg_id2)
    # msg3 = await channel.fetch_message(msg_id3)

    # await msg1.edit(content=f"Agma game server - {agma}")
    # await msg2.edit(content=f"Agma forums server - {forums}")
    # await msg3.edit(content=f"Agma backup forums server - {b_forums}")

    print("Modmail Online")

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name="Agma.io"))


blocked = []


@bot.event
async def on_message(ctx):
    guild = bot.get_guild(940455965625573386)
    category = bot.get_channel(941435672437358692)
    happy_channel = bot.get_channel(943825031920775179)

    with open('t.txt', 'r') as f:
        pbanned = f.read()

    if ctx.author == bot.user or ctx.author.id in blocked or str(
            ctx.author.id) in pbanned:
        return

    if not ctx.guild:
        cursor.execute("SELECT user_id FROM modmail WHERE user_id = (?)",
                       (ctx.author.id, ))
        if check(cursor.fetchone()) is True:
            try:
                print("RETURNING USER")
                cursor.execute(
                    "SELECT channel_id FROM modmail WHERE user_id = (?)",
                    (ctx.author.id, ))
                channel_id = cursor.fetchone()

                for id in channel_id:
                    channel_id = id
                    break
                channel = bot.get_channel(channel_id)
                if channel is None:
                    print("CHANNEL NOT FOUND")

                    new_channel = await guild.create_text_channel(
                        f"{ctx.author.name}-{ctx.author.id}",
                        category=category)

                    bot.user_id = ctx.author.id

                    cursor.execute(
                        "UPDATE modmail SET channel_id = (?) WHERE user_id = (?)",
                        (
                            new_channel.id,
                            ctx.author.id,
                        ))
                    db.commit()
                    channel = new_channel

                    discord.AllowedMentions(everyone=False)
                #User/Player relaying attachment to channel

                if ctx.attachments:
                    for attachment in ctx.attachments:
                        await channel.send(f"{ctx.author}")
                        await channel.send(f"{attachment.url}")

                #User/Player relaying message to channel

                if False:
                    pass
                else:
                    if "accept my skin" in ctx.content:
                        await channel.send(
                            "**Smart Suggestions**: It seems this user is asking for a skin approval, an answer to this question may be:"
                        )
                        await channel.send("/")
                        await channel.send(
                            ' "Please be patient, a mod will review it when they have time." (accuracy - 90%) '
                        )
                    if "change email" in ctx.content:
                        await channel.send(
                            "**Smart Suggestions**: It seems this user is asking for an account email change."
                        )
                        await channel.send(
                            'As of now, sora is too busy to handle email changes, a default response to this question is - '
                        )
                        await channel.send(
                            """Send him a message at the right place. Not Discord. Go to the Forums (agarioforums.net), and send him an e-mail. But he is on file as saying he does not want to help people change their e-mail addresses. We have been advising such people to just start a new account, and do it right this time,. If you have a lot of puchases unused on your old account, ask him instead if you can transfer them to the new account.``` """
                        )
                    await channel.send(f"(**{ctx.author}**): {ctx.content}")
                    await happy_channel.send(f"**{ctx.author}**:{ctx.content}")

            except Exception as e:
                print(e)

        else:

            try:
                print("NEW USER")
                print(ctx.content.isalpha())

                if ctx.content.isalpha():
                    await ctx.author.send(
                        "Please send a more detailed repsonse or question! That way our staff can help you as soon as possible."
                    )

                else:
                    modmail_channel = await guild.create_text_channel(
                        f"{ctx.author.name}-{ctx.author.id}",
                        category=category)

                    cursor.execute("INSERT INTO modmail VALUES (?, ?)", (
                        ctx.author.id,
                        modmail_channel.id,
                    ))
                    db.commit()
                    
                    if ctx.author.id == 462508499335774228:
                        allowed_mentions = discord.AllowedMentions(everyone=False)
                    else:
                        allowed_mentions = discord.AllowedMentions(everyone=True)

                    try:
                        await modmail_channel.send(content="@here", allowed_mentions=allowed_mentions)
                    except:
                        pass
                
                    

                    user = bot.get_user(int(ctx.author.id))

                    embed_info = discord.Embed(
                        title="User Information",
                        timestamp=datetime.datetime.utcnow(),
                        colour=discord.Colour.random())
                    embed_info.set_thumbnail(url=user.avatar.url)
                    embed_info.add_field(name="Name", value=user.name)
                    embed_info.add_field(name="ID", value=user.id)
                    embed_info.add_field(name="Account Created",
                                         value=user.created_at.strftime(
                                             "%a %#d %B %Y, %I:%M %p UTC"))
                    embed_info.add_field(name="User Notes",
                                         value="(Coming soon!) - Happy?")

                    embed_info.add_field(name="User Status", value="a")

                    await modmail_channel.send(embed=embed_info)
                    discord.AllowedMentions(everyone=False)

                    embed = discord.Embed(title="Agma.io Support Bot",
                                          description=ctx.content,
                                          color=0xFF5733)

                    embed.set_author(name=f"Agma.io User ({ctx.author.name})",
                                     icon_url=ctx.author.avatar.url)

                    embed_starter = discord.Embed(
                        title="Agma.io Support Bot",
                        description=
                        """Thank you for DM'ing the Agma.io Support Bot!
  Please message here your 
  🔸Problems 
  🔸Questions 
  🔸Complaints or 
  🔸Requests 
  Our support team is trying their best to answer all threads, please be patient and don't spam! ❤️ 
  """)
                    
                    await ctx.author.send(embed=embed_starter)
                    await modmail_channel.send(
                        f"**{ctx.author.name}**: {ctx.content}")

                if "accept my skin" in ctx.content:
                    await modmail_channel.send(
                        "**Smart Suggestions**: It seems this user is asking for a skin approval, an answer to this question may be:"
                    )
                    await modmail_channel.send("/")
                    await modmail_channel.send(
                        'Please be patient, a mod will review it when they have time.'
                    )
                if "change email" in ctx.content:
                    await modmail_channel.send(
                        "**Smart Suggestions**: It seems this user is asking for an account email change."
                    )
                    await modmail_channel.send(
                        'As of now, sora is too busy to handle email changes, a default response to this question is - '
                    )
                    await modmail_channel.send(
                        """Send him a message at the right place. Not Discord. Go to the Forums (agarioforums.net), and send him an e-mail. But he is on file as saying he does not want to help people change their e-mail addresses.

We have been advising such people to just start a new account, and do it right this time,. If you have a lot of puchases unused on your old account, ask him instead if you can transfer them to the new account.``` """
                    )

                await happy_channel.send(f"**{ctx.author}**: {ctx.content}")

                user = bot.get_user(int(ctx.author.id))

                embed_info = discord.Embed(
                    title="User Information",
                    timestamp=datetime.datetime.utcnow(),
                    colour=discord.Colour.random())
                embed_info.set_thumbnail(url=user.avatar.url)
                embed_info.add_field(name="Name", value=user.name)
                embed_info.add_field(name="ID", value=user.id)
                embed_info.add_field(name="Account Created",
                                     value=user.created_at.strftime(
                                         "%a %#d %B %Y, %I:%M %p UTC"))
                embed_info.add_field(name="User Notes",
                                     value="(Coming soon!) - Happy?")
                embed_info.add_field(name="User Status", value="b")

                await modmail_channel.send(embed=embed_info)

            except Exception as e:
                print(e)
                print("1")

    else:
        if ctx.channel.category == category:
            cursor.execute(
                "SELECT channel_id FROM modmail WHERE user_id = (?)",
                (ctx.author.id, ))
            if check(cursor.fetchone()) is True:
                try:
                    cursor.execute(
                        "SELECT user_id FROM modmail WHERE channel_id = (?)",
                        (ctx.channel.id, ))
                    user_id = cursor.fetchone()

                    for id in user_id:
                        user_id = id
                        break

                except Exception as e:
                    print(e)
                    print("2")
                    await ctx.add_reaction('❌')

        await bot.process_commands(ctx)


@bot.command(name="m")
async def messagea(ctx, *, text):
    channel_name = ctx.channel.name.split('-')
    user = bot.get_user(int(channel_name[-1]))
    """MESSAGE COMMAND"""
    if "agma.io staff" in [y.name.lower() for y in ctx.author.roles]:
        happy_channel = bot.get_channel(943825031920775179)

        embed = discord.Embed(title="Agma.io Support Bot",
                              description=text,
                              color=0xFF5733)

        embed.set_author(
            name="Agma.io Staff",
            icon_url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669001509699584/Staff_Crown.png"
        )

        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669002084352051/Agma.png"
        )
        ##########################

        await ctx.channel.purge(limit=1)
        await user.send(embed=embed)
        await ctx.channel.send(f"**Agma.io Staff({ctx.author.name})**: {text}")
        await happy_channel.send(f"**{ctx.author}(STAFF)**: {ctx.content}")
        print("STAFF sent a message")

    elif "agma.io moderator" in [y.name.lower() for y in ctx.author.roles]:
        happy_channel = bot.get_channel(943825031920775179)

        embed = discord.Embed(title="Agma.io Support Bot",
                              description=text,
                              color=0xFF5733)

        embed.set_author(
            name="Agma.io Moderator",
            icon_url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669001258057769/AgmaMods.png"
        )

        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669002084352051/Agma.png"
        )
        ##########################

        await ctx.channel.purge(limit=1)
        await user.send(embed=embed)
        await ctx.channel.send(
            f"**Agma.io Moderator({ctx.author.name})**: {text}")

    elif "agma.io support" in [y.name.lower() for y in ctx.author.roles]:
        happy_channel = bot.get_channel(943825031920775179)

        embed = discord.Embed(title="Agma.io Support Bot",
                              description=text,
                              color=0xFF5733)

        embed.set_author(
            name="Agma.io Support",
            icon_url=
            "https://cdn.discordapp.com/attachments/942665547357777940/942665740140560434/imageonline-co-transparentimage_35.png"
        )

        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669002084352051/Agma.png"
        )
        ##########################

        await ctx.channel.purge(limit=1)
        await user.send(embed=embed)
        await ctx.channel.send(
            f"**Agma.io Support({ctx.author.name})**: {text}")
        print("Message sent")

    elif "agma.io owner" in [y.name.lower() for y in ctx.author.roles]:
        happy_channel = bot.get_channel(943825031920775179)

        embed = discord.Embed(title="Agma.io Support Bot",
                              description=text,
                              color=0xFF5733)

        embed.set_author(
            name="Agma.io Admin",
            icon_url=
            "https://cdn.discordapp.com/attachments/942665547357777940/942672927034331167/701119381559574558.webp"
        )

        await ctx.channel.purge(limit=1)
        await user.send(embed=embed)
        await ctx.channel.send(f"**Agma.io Admin({ctx.author.name})**: {text}")
        await happy_channel.send(f"**{ctx.author}(ADMIN)**: {ctx.content}")
        print("OWNER sent a message")

    else:
        await ctx.channel.send(
            "ERROR: YOU DO NOT HAVE PERMISSIONS TO PERFORM THIS ACTION. (PermissionError (If you are a registered support user please message 'Happy?#5111')) ❌"
        )
        print("Message error (PermissionError) user - " + str(ctx.author))


@bot.command(name="close")
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def closed(ctx):
    try:
        channel_cls = ctx.channel
        channel_name = ctx.channel.name.split('-')
        user = bot.get_user(int(channel_name[-1]))

        embed = discord.Embed(
            title="Agma.io Support Bot",
            description=
            "Your thread has been closed by a staff member, Messaging this bot again will start another support thread.",
            color=0xFF5733)

        embed.set_author(name="Agma.io Staff Team")

        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669002084352051/Agma.png"
        )

        await user.send(embed=embed)

        await channel_cls.delete()
        log_channel = bot.get_channel(942762723199045692)
        await log_channel.send(f"{ctx.author} has closed the channel {ctx.channel}"
                            )
        cursor.execute("DELETE FROM modmail WHERE channel_id = (?)",
                    (channel_cls.id, ))
        db.commit()
        print("Channel closed")
    except Exception as e:
        await ctx.channel.send(e)
        await ctx.channel.send("Error code FORBIDDEN 403")


    @bot.command()
    async def archive(ctx, name):

        guild = bot.get_guild(940455965625573386)
        category_arch = bot.get_channel(941885374375030815)
        arch_channel = await guild.create_text_channel(f"{name}",
                                                    category=category_arch)

        messages = await ctx.channel.history(limit=200).flatten()
        #Removing the @here statement from history.
        messages.pop(-1)

        for msg in reversed(messages):
            if msg.attachments:
                await arch_channel.send(f"{msg.attachments.url}")
            else:
                await arch_channel.send(msg.content)

        await ctx.channel.send("Thread archived ✅ ")
        print("Channel Archived")

        log_channel = bot.get_channel(942762723199045692)

        await log_channel.send(
            f"{ctx.author.mention} has archived a thread with the name of - {name}"
        )


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def ping(ctx):
    await ctx.channel.send("Pong!")


@bot.command()
@commands.has_any_role("Agma.io Owner", "Agma.io Staff", "Bot Creator",
                       "Agma.io Support")
async def tban(ctx, userId, *, reason):
    log_channel = bot.get_channel(942762723199045692)
    await log_channel.send(
        f"**{userId}** has been temporarily blocked by {ctx.author.mention} ```reason: {reason}```"
    )
    await ctx.channel.send(
        f"You have blocked {userId} for reason: **{reason}**")
    user = bot.get_user(int(userId))
    await user.send(
        f"**YOU HAVE BEEN TEMPORARILY BLOCKED FROM USING THE BOTS SERVICES ❌**) ```reason: {reason}```"
    )
    blocked.append(int(userId))


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def blist(ctx):
    counter = 0
    with open('t.txt', 'r') as f:
        txt_ids = f.readlines()

    await ctx.channel.send("Temporary Block List")
    for block in blocked:
        counter += 1
        await ctx.channel.send(f"**{counter}:** {str(block)}")
    await ctx.channel.send("```...```")

    await ctx.channel.send("Permanant Block List")
    counter = 0
    for i in txt_ids:
        counter += 1
        await ctx.channel.send(f"**{counter}:** {i}")


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Bot Creator",
                       "Agma.io Support")
async def pban(ctx, userID, *, reason):
    log_channel = bot.get_channel(942762723199045692)
    with open('t.txt', 'a') as f:
        f.write(f"{userID}\n")
    await ctx.channel.send(f"**{userID}** has been blocked.")

    await log_channel.send(
        f"**{userID}** has been permanently blocked by {ctx.author.mention} ```reason: {reason}```"
    )

    await ctx.channel.send(
        f"You have blocked {userID} for reason: **{reason}**")

    user = bot.get_user(int(userID))

    await user.send(
        f"**YOU HAVE BEEN PERMANENTLY BLOCKED FROM USING THE BOTS SERVICES ❌**) ```reason: {reason}```"
    )


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def get(ctx):
    await ctx.channel.send(ctx.channel.name)
    channel_name = ctx.channel.name.split('-')
    await ctx.channel.send(channel_name)
    await ctx.channel.send(channel_name[-1])


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def update_mode(ctx):

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="Down for updates :)"))
    await ctx.channel.send("Entering update mode...")


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def exit_update_mode(ctx):
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="For People who need help...")
                              )
    await ctx.channel.send("Exiting update mode...")


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def help(ctx):
    await ctx.channel.send("""```
                              COMMANDS LIST

KEYS:
* = Optional
^ = Mandatory 


COMMANDS:

?!m - Message command to message the user. (Support/Mod/Staff/Admin Use)

?!help - shows this command (Support/Mod/Staff/Admin Use)

?!update_mode - Enters update mode (Bot dev/Admin use)

?!shutdown_agmabot_True - Turns off the bot for an hour (Bot dev/Admin Use)

?!archive (channel name^) - Makes a copy of the current thread the command was used in (Support/Staff/Bot Dev/Admin Use)

?!exit_update_mode - Exits out of update mode (Bot dev/Admin Use)

?!note (id*) - Pulls up Past notes of the user. (Support/Staff/Bot Dev/Admin Use)

?!notew (id*) (text^) - Write a note about a user. (Support/Staff/Bot Dev/Admin Use)

?!close - Closes the thread. (Support/Staff/Bot Dev/Admin Use)

?!ping - Pings the bot, Usually used for testing. (Support/Staff/Bot Dev/Admin Use)

?!pban (id^) (reason^) - Bans the user permanently (Staff/Bot dev/Admin Use)

?!tban (id^) (reason^) - Bans the user for 24 hours. (Support/Staff/Bot Dev/Admin Use)
```
                   """)


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def note(ctx):
    await ctx.channel.send("Establishing a connection with Note bot...")
    await ctx.channel.send(
        "CONNECTION FAILED (Code error 6005) - Send Owner error code.")


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Bot Creator")
async def shutdown_agmabot_True(ctx):
    await ctx.channel.send("Shutting down for 100000 seconds")
    time.sleep(100000)


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def stats_db(ctx):
    await ctx.channel.send("Sending stats of modmail.db")

    cursor.execute("SELECT * FROM modmail")
    try:
        await ctx.channel.send(cursor.fetchall())
    except:
        await ctx.channel.send("Database corrupted.")




@bot.command(name="uid")
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support", "Agma.io Moderator", "Bot Creator")
async def tex(ctx):
    channel_name = ctx.channel.name.split('-')
    await ctx.channel.send(channel_name[-1])

@bot.command(name="mclose")
@commands.has_any_role('Agma.io Owner', "Bot Creator")
async def tex(ctx):

    channel_cls = ctx.channel

    cursor.execute("DELETE FROM modmail WHERE channel_id = (?)",
                    (channel_cls.id, ))
    db.commit()

    await channel_cls.delete()


def translation(text, d=None):
    t = Translator()
    if d is None:
        d='en'
    tr = t.translate(str(text), dest=d )
    print(tr)
    return tr.text



@bot.command(name="translate")
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support", "Agma.io Moderator", "Bot Creator")
async def translate(ctx):
    guild = bot.get_guild(940455965625573386)

    messages = await ctx.channel.history(limit=200).flatten()
        #Removing the @here statement from history and embed.
    messages.pop(-1)
    messages.pop(-1)

    for msg in reversed(messages):
        if msg.attachments:
            continue
        else:
            await ctx.channel.send(translation(msg))



bot.run(token)
fix="?!", intents=discord.Intents.all())

bot.remove_command('help')

agma_id = 356145230342389760

db = sqlite3.connect('modmail.db')
cursor = db.cursor()

# Remove after running once
# cursor.execute("""
#     CREATE TABLE modmail (
#         user_id int,
#         channel_id int
#      )
# """)


def check(key):
    if key is None:
        return False
    else:
        return True


bot.user_id = None


@bot.event
async def on_ready():

    # agma, forums, b_forums = status()

    # channel = bot.get_channel(512586535011483648)  # the message's channel

    # msg_id1 = 971028738772971520
    # msg_id2 = 971028739490205777
    # msg_id3 = 973900585357156373

    # if agma != 200:
    #     agma = "❌"
    # elif agma == 200:
    #     agma = "✅"

    # if b_forums != 200:
    #     b_forums = "❌"
    # elif b_forums == 200:
    #     b_forums = "✅"

    # if forums != 200:
    #     forums = "❌"
    # elif forums == 200:
    #     forums = "✅"

    # msg1 = await channel.fetch_message(msg_id1)
    # msg2 = await channel.fetch_message(msg_id2)
    # msg3 = await channel.fetch_message(msg_id3)

    # await msg1.edit(content=f"Agma game server - {agma}")
    # await msg2.edit(content=f"Agma forums server - {forums}")
    # await msg3.edit(content=f"Agma backup forums server - {b_forums}")

    print("Modmail Online")

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name="Agma.io"))


blocked = []


@bot.event
async def on_message(ctx):
    guild = bot.get_guild(940455965625573386)
    category = bot.get_channel(941435672437358692)
    happy_channel = bot.get_channel(943825031920775179)

    with open('t.txt', 'r') as f:
        pbanned = f.read()

    if ctx.author == bot.user or ctx.author.id in blocked or str(
            ctx.author.id) in pbanned:
        return

    if not ctx.guild:
        cursor.execute("SELECT user_id FROM modmail WHERE user_id = (?)",
                       (ctx.author.id, ))
        if check(cursor.fetchone()) is True:
            try:
                print("RETURNING USER")
                cursor.execute(
                    "SELECT channel_id FROM modmail WHERE user_id = (?)",
                    (ctx.author.id, ))
                channel_id = cursor.fetchone()

                for id in channel_id:
                    channel_id = id
                    break
                channel = bot.get_channel(channel_id)
                if channel is None:
                    print("CHANNEL NOT FOUND")

                    new_channel = await guild.create_text_channel(
                        f"{ctx.author.name}-{ctx.author.id}",
                        category=category)

                    bot.user_id = ctx.author.id

                    cursor.execute(
                        "UPDATE modmail SET channel_id = (?) WHERE user_id = (?)",
                        (
                            new_channel.id,
                            ctx.author.id,
                        ))
                    db.commit()
                    channel = new_channel

                    discord.AllowedMentions(everyone=False)
                #User/Player relaying attachment to channel

                if ctx.attachments:
                    for attachment in ctx.attachments:
                        await channel.send(f"{ctx.author}")
                        await channel.send(f"{attachment.url}")

                #User/Player relaying message to channel

                if False:
                    pass
                else:
                    await ctx.add_reaction('✅')
                    if "accept my skin" in ctx.content:
                        await channel.send(
                            "**Smart Suggestions**: It seems this user is asking for a skin approval, an answer to this question may be:"
                        )
                        await channel.send("/")
                        await channel.send(
                            ' "Please be patient, a mod will review it when they have time." (accuracy - 90%) '
                        )
                    if "change email" in ctx.content:
                        await channel.send(
                            "**Smart Suggestions**: It seems this user is asking for an account email change."
                        )
                        await channel.send(
                            'As of now, sora is too busy to handle email changes, a default response to this question is - '
                        )
                        await channel.send(
                            """Send him a message at the right place. Not Discord. Go to the Forums (agarioforums.net), and send him an e-mail. But he is on file as saying he does not want to help people change their e-mail addresses. We have been advising such people to just start a new account, and do it right this time,. If you have a lot of puchases unused on your old account, ask him instead if you can transfer them to the new account.``` """
                        )
                    await channel.send(f"(**{ctx.author}**): {ctx.content}")
                    await happy_channel.send(f"**{ctx.author}**:{ctx.content}")

            except Exception as e:
                print(e)

        else:

            try:
                print("NEW USER")
                print(ctx.content.isalpha())

                if ctx.content.isalpha():
                    await ctx.author.send(
                        "Please send a more detailed repsonse or question! That way our staff can help you as soon as possible."
                    )

                else:
                    modmail_channel = await guild.create_text_channel(
                        f"{ctx.author.name}-{ctx.author.id}",
                        category=category)

                    cursor.execute("INSERT INTO modmail VALUES (?, ?)", (
                        ctx.author.id,
                        modmail_channel.id,
                    ))
                    db.commit()
                    
                    if ctx.author.id == 462508499335774228:
                        allowed_mentions = discord.AllowedMentions(everyone=False)
                    else:
                        allowed_mentions = discord.AllowedMentions(everyone=True)

                    try:
                        await modmail_channel.send(content="@here", allowed_mentions=allowed_mentions)
                    except:
                        pass
                
                    

                    user = bot.get_user(int(ctx.author.id))

                    embed_info = discord.Embed(
                        title="User Information",
                        timestamp=datetime.datetime.utcnow(),
                        colour=discord.Colour.random())
                    embed_info.set_thumbnail(url=user.avatar.url)
                    embed_info.add_field(name="Name", value=user.name)
                    embed_info.add_field(name="ID", value=user.id)
                    embed_info.add_field(name="Account Created",
                                         value=user.created_at.strftime(
                                             "%a %#d %B %Y, %I:%M %p UTC"))
                    embed_info.add_field(name="User Notes",
                                         value="(Coming soon!) - Happy?")

                    embed_info.add_field(name="User Status", value="a")

                    await modmail_channel.send(embed=embed_info)
                    discord.AllowedMentions(everyone=False)

                    embed = discord.Embed(title="Agma.io Support Bot",
                                          description=ctx.content,
                                          color=0xFF5733)

                    embed.set_author(name=f"Agma.io User ({ctx.author.name})",
                                     icon_url=ctx.author.avatar.url)

                    embed_starter = discord.Embed(
                        title="Agma.io Support Bot",
                        description=
                        """Thank you for DM'ing the Agma.io Support Bot!
  Please message here your 
  🔸Problems 
  🔸Questions 
  🔸Complaints or 
  🔸Requests 
  Our support team is trying their best to answer all threads, please be patient and don't spam! ❤️ 
  """)
                    await ctx.add_reaction('✅')
                    await ctx.author.send(embed=embed_starter)
                    await modmail_channel.send(
                        f"**{ctx.author.name}**: {ctx.content}")

                if "accept my skin" in ctx.content:
                    await modmail_channel.send(
                        "**Smart Suggestions**: It seems this user is asking for a skin approval, an answer to this question may be:"
                    )
                    await modmail_channel.send("/")
                    await modmail_channel.send(
                        'Please be patient, a mod will review it when they have time.'
                    )
                if "change email" in ctx.content:
                    await modmail_channel.send(
                        "**Smart Suggestions**: It seems this user is asking for an account email change."
                    )
                    await modmail_channel.send(
                        'As of now, sora is too busy to handle email changes, a default response to this question is - '
                    )
                    await modmail_channel.send(
                        """Send him a message at the right place. Not Discord. Go to the Forums (agarioforums.net), and send him an e-mail. But he is on file as saying he does not want to help people change their e-mail addresses.

We have been advising such people to just start a new account, and do it right this time,. If you have a lot of puchases unused on your old account, ask him instead if you can transfer them to the new account.``` """
                    )

                await happy_channel.send(f"**{ctx.author}**: {ctx.content}")

                user = bot.get_user(int(ctx.author.id))

                embed_info = discord.Embed(
                    title="User Information",
                    timestamp=datetime.datetime.utcnow(),
                    colour=discord.Colour.random())
                embed_info.set_thumbnail(url=user.avatar.url)
                embed_info.add_field(name="Name", value=user.name)
                embed_info.add_field(name="ID", value=user.id)
                embed_info.add_field(name="Account Created",
                                     value=user.created_at.strftime(
                                         "%a %#d %B %Y, %I:%M %p UTC"))
                embed_info.add_field(name="User Notes",
                                     value="(Coming soon!) - Happy?")
                embed_info.add_field(name="User Status", value="b")

                await modmail_channel.send(embed=embed_info)

            except Exception as e:
                print(e)
                print("1")
                await ctx.add_reaction('❌')

    else:
        if ctx.channel.category == category:
            cursor.execute(
                "SELECT channel_id FROM modmail WHERE user_id = (?)",
                (ctx.author.id, ))
            if check(cursor.fetchone()) is True:
                try:
                    cursor.execute(
                        "SELECT user_id FROM modmail WHERE channel_id = (?)",
                        (ctx.channel.id, ))
                    user_id = cursor.fetchone()

                    for id in user_id:
                        user_id = id
                        break

                except Exception as e:
                    print(e)
                    print("2")
                    await ctx.add_reaction('❌')

        await bot.process_commands(ctx)


@bot.command(name="m")
async def messagea(ctx, *, text):
    channel_name = ctx.channel.name.split('-')
    user = bot.get_user(int(channel_name[-1]))
    """MESSAGE COMMAND"""
    if "agma.io staff" in [y.name.lower() for y in ctx.author.roles]:
        happy_channel = bot.get_channel(943825031920775179)

        embed = discord.Embed(title="Agma.io Support Bot",
                              description=text,
                              color=0xFF5733)

        embed.set_author(
            name="Agma.io Staff",
            icon_url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669001509699584/Staff_Crown.png"
        )

        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669002084352051/Agma.png"
        )
        ##########################

        await ctx.channel.purge(limit=1)
        await user.send(embed=embed)
        await ctx.channel.send(f"**Agma.io Staff({ctx.author.name})**: {text}")
        await happy_channel.send(f"**{ctx.author}(STAFF)**: {ctx.content}")
        print("STAFF sent a message")

    elif "agma.io moderator" in [y.name.lower() for y in ctx.author.roles]:
        happy_channel = bot.get_channel(943825031920775179)

        embed = discord.Embed(title="Agma.io Support Bot",
                              description=text,
                              color=0xFF5733)

        embed.set_author(
            name="Agma.io Moderator",
            icon_url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669001258057769/AgmaMods.png"
        )

        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669002084352051/Agma.png"
        )
        ##########################

        await ctx.channel.purge(limit=1)
        await user.send(embed=embed)
        await ctx.channel.send(
            f"**Agma.io Moderator({ctx.author.name})**: {text}")

    elif "agma.io support" in [y.name.lower() for y in ctx.author.roles]:
        happy_channel = bot.get_channel(943825031920775179)

        embed = discord.Embed(title="Agma.io Support Bot",
                              description=text,
                              color=0xFF5733)

        embed.set_author(
            name="Agma.io Support",
            icon_url=
            "https://cdn.discordapp.com/attachments/942665547357777940/942665740140560434/imageonline-co-transparentimage_35.png"
        )

        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669002084352051/Agma.png"
        )
        ##########################

        await ctx.channel.purge(limit=1)
        await user.send(embed=embed)
        await ctx.channel.send(
            f"**Agma.io Support({ctx.author.name})**: {text}")
        print("Message sent")

    elif "agma.io owner" in [y.name.lower() for y in ctx.author.roles]:
        happy_channel = bot.get_channel(943825031920775179)

        embed = discord.Embed(title="Agma.io Support Bot",
                              description=text,
                              color=0xFF5733)

        embed.set_author(
            name="Agma.io Admin",
            icon_url=
            "https://cdn.discordapp.com/attachments/942665547357777940/942672927034331167/701119381559574558.webp"
        )

        await ctx.channel.purge(limit=1)
        await user.send(embed=embed)
        await ctx.channel.send(f"**Agma.io Admin({ctx.author.name})**: {text}")
        await happy_channel.send(f"**{ctx.author}(ADMIN)**: {ctx.content}")
        print("OWNER sent a message")

    else:
        await ctx.channel.send(
            "ERROR: YOU DO NOT HAVE PERMISSIONS TO PERFORM THIS ACTION. (PermissionError (If you are a registered support user please message 'Happy?#5111')) ❌"
        )
        print("Message error (PermissionError) user - " + str(ctx.author))


@bot.command(name="close")
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def closed(ctx):
    try:
        channel_cls = ctx.channel
        channel_name = ctx.channel.name.split('-')
        user = bot.get_user(int(channel_name[-1]))

        embed = discord.Embed(
            title="Agma.io Support Bot",
            description=
            "Your thread has been closed by a staff member, Messaging this bot again will start another support thread.",
            color=0xFF5733)

        embed.set_author(name="Agma.io Staff Team")

        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/942143239631302656/942669002084352051/Agma.png"
        )

        await user.send(embed=embed)

        await channel_cls.delete()
        log_channel = bot.get_channel(942762723199045692)
        await log_channel.send(f"{ctx.author} has closed the channel {ctx.channel}"
                            )
        cursor.execute("DELETE FROM modmail WHERE channel_id = (?)",
                    (channel_cls.id, ))
        db.commit()
        print("Channel closed")
    except Exception as e:
        await ctx.channel.send(e)
        await ctx.channel.send("Error code FORBIDDEN 403")


    @bot.command()
    async def archive(ctx, name):

        guild = bot.get_guild(940455965625573386)
        category_arch = bot.get_channel(941885374375030815)
        arch_channel = await guild.create_text_channel(f"{name}",
                                                    category=category_arch)

        messages = await ctx.channel.history(limit=200).flatten()
        #Removing the @here statement from history.
        messages.pop(-1)

        for msg in reversed(messages):
            if msg.attachments:
                await arch_channel.send(f"{msg.attachments.url}")
            else:
                await arch_channel.send(msg.content)

        await ctx.channel.send("Thread archived ✅ ")
        print("Channel Archived")

        log_channel = bot.get_channel(942762723199045692)

        await log_channel.send(
            f"{ctx.author.mention} has archived a thread with the name of - {name}"
        )


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def ping(ctx):
    await ctx.channel.send("Pong!")


@bot.command()
@commands.has_any_role("Agma.io Owner", "Agma.io Staff", "Bot Creator",
                       "Agma.io Support")
async def tban(ctx, userId, *, reason):
    log_channel = bot.get_channel(942762723199045692)
    await log_channel.send(
        f"**{userId}** has been temporarily blocked by {ctx.author.mention} ```reason: {reason}```"
    )
    await ctx.channel.send(
        f"You have blocked {userId} for reason: **{reason}**")
    user = bot.get_user(int(userId))
    await user.send(
        f"**YOU HAVE BEEN TEMPORARILY BLOCKED FROM USING THE BOTS SERVICES ❌**) ```reason: {reason}```"
    )
    blocked.append(int(userId))


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def blist(ctx):
    counter = 0
    with open('t.txt', 'r') as f:
        txt_ids = f.readlines()

    await ctx.channel.send("Temporary Block List")
    for block in blocked:
        counter += 1
        await ctx.channel.send(f"**{counter}:** {str(block)}")
    await ctx.channel.send("```...```")

    await ctx.channel.send("Permanant Block List")
    counter = 0
    for i in txt_ids:
        counter += 1
        await ctx.channel.send(f"**{counter}:** {i}")


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Bot Creator",
                       "Agma.io Support")
async def pban(ctx, userID, *, reason):
    log_channel = bot.get_channel(942762723199045692)
    with open('t.txt', 'a') as f:
        f.write(f"{userID}\n")
    await ctx.channel.send(f"**{userID}** has been blocked.")

    await log_channel.send(
        f"**{userID}** has been permanently blocked by {ctx.author.mention} ```reason: {reason}```"
    )

    await ctx.channel.send(
        f"You have blocked {userID} for reason: **{reason}**")

    user = bot.get_user(int(userID))

    await user.send(
        f"**YOU HAVE BEEN PERMANENTLY BLOCKED FROM USING THE BOTS SERVICES ❌**) ```reason: {reason}```"
    )


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def get(ctx):
    await ctx.channel.send(ctx.channel.name)
    channel_name = ctx.channel.name.split('-')
    await ctx.channel.send(channel_name)
    await ctx.channel.send(channel_name[-1])


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def update_mode(ctx):

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="Down for updates :)"))
    await ctx.channel.send("Entering update mode...")


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def exit_update_mode(ctx):
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="For People who need help...")
                              )
    await ctx.channel.send("Exiting update mode...")


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def help(ctx):
    await ctx.channel.send("""```
                              COMMANDS LIST

KEYS:
* = Optional
^ = Mandatory 


COMMANDS:

?!m - Message command to message the user. (Support/Mod/Staff/Admin Use)

?!help - shows this command (Support/Mod/Staff/Admin Use)

?!update_mode - Enters update mode (Bot dev/Admin use)

?!shutdown_agmabot_True - Turns off the bot for an hour (Bot dev/Admin Use)

?!archive (channel name^) - Makes a copy of the current thread the command was used in (Support/Staff/Bot Dev/Admin Use)

?!exit_update_mode - Exits out of update mode (Bot dev/Admin Use)

?!note (id*) - Pulls up Past notes of the user. (Support/Staff/Bot Dev/Admin Use)

?!notew (id*) (text^) - Write a note about a user. (Support/Staff/Bot Dev/Admin Use)

?!close - Closes the thread. (Support/Staff/Bot Dev/Admin Use)

?!ping - Pings the bot, Usually used for testing. (Support/Staff/Bot Dev/Admin Use)

?!pban (id^) (reason^) - Bans the user permanently (Staff/Bot dev/Admin Use)

?!tban (id^) (reason^) - Bans the user for 24 hours. (Support/Staff/Bot Dev/Admin Use)
```
                   """)


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def note(ctx):
    await ctx.channel.send("Establishing a connection with Note bot...")
    await ctx.channel.send(
        "CONNECTION FAILED (Code error 6005) - Send Owner error code.")


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Bot Creator")
async def shutdown_agmabot_True(ctx):
    await ctx.channel.send("Shutting down for 100000 seconds")
    time.sleep(100000)


@bot.command()
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support",
                       "Agma.io Moderator", "Bot Creator")
async def stats_db(ctx):
    await ctx.channel.send("Sending stats of modmail.db")

    cursor.execute("SELECT * FROM modmail")
    try:
        await ctx.channel.send(cursor.fetchall())
    except:
        await ctx.channel.send("Database corrupted.")




@bot.command(name="uid")
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support", "Agma.io Moderator", "Bot Creator")
async def tex(ctx):
    channel_name = ctx.channel.name.split('-')
    await ctx.channel.send(channel_name[-1])

@bot.command(name="mclose")
@commands.has_any_role('Agma.io Owner', "Bot Creator")
async def tex(ctx):

    channel_cls = ctx.channel

    cursor.execute("DELETE FROM modmail WHERE channel_id = (?)",
                    (channel_cls.id, ))
    db.commit()

    await channel_cls.delete()


def translation(text, d=None):
    t = Translator()
    if d is None:
        d='en'
    tr = t.translate(str(text), dest=d )
    print(tr)
    return tr.text



@bot.command(name="translate")
@commands.has_any_role('Agma.io Owner', "Agma.io Staff", "Agma.io Support", "Agma.io Moderator", "Bot Creator")
async def translate(ctx):
    guild = bot.get_guild(940455965625573386)

    messages = await ctx.channel.history(limit=200).flatten()
        #Removing the @here statement from history and embed.
    messages.pop(-1)
    messages.pop(-1)

    for msg in reversed(messages):
        if msg.attachments:
            continue
        else:
            await ctx.channel.send(translation(msg))



bot.run(token)
