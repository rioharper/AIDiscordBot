import discord
import asyncio
from discord.commands import Option
import computeMessages
import computeVoice
from jsonfunk import *
import datasetgen

intents = discord.Intents.all()
bot = discord.Bot(intents=intents) #init discord bot
DISCORD_TOKEN = ""

bot.prompts=getNames() #get the names of all prompts in the prompts.json file, will refresh on restart, or if the file is edited
bot.engines = getEngines()

bot.temp = 1.1
bot.max_tokens = 125
bot.presence_penalty = 0.1
bot.backforths= 5

params = ["temp", "max_tokens", "presence_penalty", "backforths"]


@bot.event
async def on_ready(): #when bot is ready
    print("Bot is ready!")
    await bot.change_presence(activity=discord.Game(name="Status: Ready To Roll"))

@bot.slash_command(guild_ids=[], description="start a conversation with the AI")
async def talk(ctx,
format: Option(str, "How you communicate with the bot",choices=["voice", "text"]), 
#prompt: Option(str, "Choose a prompt for the conversation",choices=bot.prompts), 
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



@bot.slash_command(guild_ids=[], description="view the currently saved prompts")
async def viewprompts(ctx,
name: Option(str, "view one of the following prompts", choices=bot.prompts)):
    if(name == "view all"):
        await ctx.send("The following prompts are available: " + getNames())
    else:
        await ctx.send(getPrompt(name))

@bot.slash_command(guild_ids=[], description="add a new prompt to the bot")
async def addprompt(ctx,
name: Option(str, "name of the prompt"),
):
    await ctx.send("message below the prompt for the prompt " + name + ":")
    while(True):
        msg = await bot.wait_for('message')
        if(msg.author == ctx.author):
            print("Prompt " + name + " added.")
            addpromptJson(name, msg.content, ctx.author.name)
            await ctx.send("Prompt " + name + " added.")    
            break
    bot.prompts = getNames()

@bot.slash_command(guild_ids=[], description="remove a created prompt")
async def removeprompt(ctx,
name: Option(str, "remove one of the following prompts", choices=bot.prompts)):
    print("removing" + name)
    removeprompt(name)
    await ctx.send("prompt '" + name + "' removed")
    bot.prompts = getNames()

@bot.slash_command(guild_ids=[], description="add a new engine to the bot")
async def addengine(ctx,
name: Option(str, "name to view on discord"),
engine: Option(str, "engine string")
):
    addEngine(name, engine, ctx.author.name)
    await ctx.send("Engine added")
    bot.engines = getEngines()

@bot.slash_command(guild_ids=[], description="remove a created engine")
async def removeengine(ctx,
name: Option(str, "remove one of the following engines", choices=bot.engines)):
    print("removing" + name)
    removeEngine(name)
    await ctx.send("Engine '" + name + "' removed")
    bot.engines = getEngines()


@bot.slash_command(guild_ids=[], description="change generation parameters")
async def changeparms(ctx,
name: Option(str, "choose parameter to change", choices=params),
value: Option(int, "value to change parameter to")
):
    for param in params:
        if(param == name):
            paran = "bot." + param
            exec(paran + " = " + str(value))
            print(paran + " = " + str(value))
            await ctx.respond(name + " set to " + str(value))

@bot.slash_command(guild_ids=[], description="view generation parameters")
async def viewparams(ctx,
):
    await ctx.respond("temperature: " + str(bot.temp) + "\nmax_tokens: " + str(bot.max_tokens) + "\npresence_penalty: " + str(bot.presence_penalty) + "\nbackforths: " + str(bot.backforths))

@bot.slash_command(guild_ids=[], description="generate a dataset for more advanced AI responces")
async def datasetgenerator(ctx,
name: Option(str, "choose parameter to change"),
type: Option(str, "type of dataset input", choices =["Question", "Prompt"]),
):
    if type == "Question": client = datasetgen.question(name, ctx)
    else: client = datasetgen.prompt(name, ctx)
    await ctx.respond("You have already generated: " + str(client.sendCount()))
    input = None
    while input != "stop":
        input = await client.get_answer(bot)


bot.run(DISCORD_TOKEN)

