import discord
import asyncio
from discord.commands import Option
import computeMessages
import computeVoice
from jsonfunk import *

intents = discord.Intents.all()
bot = discord.Bot(intents=intents) #init discord bot

#bot.prompts=getNames() #get the names of all prompts in the prompts.json file, will refresh on restart, or if the file is edited
bot.engines = getEngines()

params = ["temp", "max_tokens", "presence_penalty", "backforths"]

args = setconfig()

temp = args["genparams"]["temp"]
max_tokens = args["genparams"]["max_tokens"]
presence_penalty = args["genparams"]["presence_penalty"]
backforths= args["genparams"]["backforths"]

vcenabled = args["voice"]["enabled"]
textenabled = args["text"]["enabled"]
commchoices = []
if vcenabled == True:
    commchoices.append("voice")
if textenabled == True:
    commchoices.append("text")

serverids = args["keys"]["guild_ids"]

@bot.event
async def on_ready(): #when bot is ready
    print("Bot is ready!")
    await bot.change_presence(activity=discord.Game(name="Status: Ready To Roll"))

@bot.slash_command(guild_ids=serverids, description="start a conversation with the AI")
async def talk(ctx,
format: Option(str, "How you communicate with the bot",choices=commchoices), 
engine: Option(str, "Choose an engine for the conversation", choices=bot.engines)
):
    if ctx.author.voice and format=="voice":
        print("You speak voice with the bot.")
        voice = ctx.author.voice
        vc = await voice.channel.connect()
        vcconvo = computeVoice.aud(engine, ctx, vc)
        await ctx.respond("------Starting Conversation------")
        vc.start_recording(
            discord.sinks.RecSink(),
            vcconvo.savefile,
            ctx.channel,
        )
        while(True):
            if(vc.check_if_recording() == False):
                vc.start_recording(
                    discord.sinks.RecSink(),
                    vcconvo.savefile,
                    ctx.channel,
                )
            elif(vcconvo.checkUserStatus() == True):
                break
            await asyncio.sleep(0.05)
        await ctx.voice_client.disconnect()

    elif format == "voice":
        await ctx.send("You are not in a voice channel") 
    else:
            txtconvo = computeMessages.ai(engine, ctx)
            await ctx.respond("------Starting Conversation------")
            while(True):
                if await txtconvo.getmsg(bot) == False: break



# @bot.slash_command(guild_ids=serverids, description="view the currently saved prompts")
# async def viewprompts(ctx,
# name: Option(str, "view one of the followifalseg prompts", choices=bot.prompts)):
#     if(name == "view all"):
#         await ctx.send("The following prompts are available: " + getNames())
#     else:
#         await ctx.send(getPrompt(name))

# @bot.slash_command(guild_ids=serverids, description="add a new prompt to the bot")
# async def addprompt(ctx,
# name: Option(str, "name of the prompt"),
# ):
#     await ctx.send("message below the prompt for the prompt " + name + ":")
#     while(True):
#         msg = await bot.wait_for('message')
#         if(msg.author == ctx.author):
#             print("Prompt " + name + " added.")
#             addpromptJson(name, msg.content, ctx.author.name)
#             await ctx.send("Prompt " + name + " added.")    
#             break
#     bot.prompts = getNames()

# @bot.slash_command(guild_ids=serverids, description="remove a created prompt")
# async def removeprompt(ctx,
# name: Option(str, "remove one of the following prompts", choices=bot.prompts)):
#     print("removing" + name)
#     removeprompt(name)
#     await ctx.send("prompt '" + name + "' removed")
#     bot.prompts = getNames()

@bot.slash_command(guild_ids=serverids, description="add a new engine to the bot")
async def addengine(ctx,
name: Option(str, "name to view on discord"),
engine: Option(str, "engine string")
):
    addEngine(name, engine, ctx.author.name)
    await ctx.send("Engine added")
    bot.engines = getEngines()

@bot.slash_command(guild_ids=serverids, description="remove a created engine")
async def removeengine(ctx,
name: Option(str, "remove one of the following engines", choices=bot.engines)):
    print("removing" + name)
    removeEngine(name)
    await ctx.send("Engine '" + name + "' removed")
    bot.engines = getEngines()

@bot.slash_command(guild_ids=serverids, description="view generation parameters")
async def viewparams(ctx,
):
    await ctx.respond("temperature: " + str(temp) + "\nmax_tokens: " + str(max_tokens) + "\npresence_penalty: " + str(presence_penalty) + "\nbackforths: " + str(backforths))

bot.run(args["keys"]["discordtoken"])

