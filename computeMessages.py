import openai
import time
import discord
import os
from jsonfunk import *



stop=["\n", "AI:"]
endconvos=["stop", "goodbye", "bye", "Stop conversation.", "see you" "Stop.", "Bye.", "Goodbye.", "See you."]
Human = "\nHuman: "
Bot = "\nAI:"

intents = discord.Intents.all()
intents.message_content = True
bot = discord.Bot(intents=intents) #init discord bot

openai.api_key = "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"

bot.temp = 0.8
bot.max_tokens = 125
bot.presence_penalty = 0.25
bot.backforths= 8

class ai(): #ai methods that all communication classes inherit
    def __init__(self, model, ctx):
        self.prompt = ""
        self.log = self.prompt
        self.model = getEngine(model)
        self.ctx = ctx
        self.filename = "chatlog-"+ str(time.strftime("%Y%m%d-%H%M%S"))+".txt"
        self.reps = 0
        f = open(self.filename, "w")
        f.write("Engine: " + self.model+"\n") #write to logfile
        f.close()
        self.stopconvo = False

    def writeToChatLog(self, input, response): 
        with open(self.filename, "a+") as f:
            data = f.read()
            data+= "\n" + "Human: " + input + "\nAI:" + response
            f.write(data) #write to logfile

    async def endConvo(self, input): #ends the current conversation, deletes any convo files, then uploads the log file to the discord channel
        if input in endconvos: 
            print("stopping chat")
            await self.ctx.send(file=discord.File(self.filename))
            await self.ctx.send("------Stopping Conversation. You can view the chatlog above------")
            os.remove(self.filename)
            self.stopconvo = True
            return True
        return False

    def checkUserStatus(self):
        return self.stopconvo

    def genresp(self):
        response = openai.Completion.create(
            model=self.model,
            prompt=self.log,
            temperature=bot.temp,
            max_tokens=bot.max_tokens,
            presence_penalty = bot.presence_penalty,
            stop=[" END", "\nAI:", "\nHuman:", "\nEND"]
        )
        return str(response.choices[0]['text'])


    async def resp(self, input): #contacts openAI engine to get a response to the user input
        print("Human: " + input)
        if self.reps % bot.backforths == 0 and self.reps != 0:
            self.log = self.prompt + Human + input + Bot
            print("log cleared")
        else: self.log += Human + input + Bot
        async with self.ctx.typing():
            responce = self.genresp()
        await self.ctx.send(responce)
        self.log+= responce
        self.writeToChatLog(input, responce)
        print("AI: " + responce)
        print("LOG: " + self.log)
        self.reps += 1
        return responce

    async def getmsg(self, bot): #listens to the user input from the discord channel
        while(True):
            try:
                msg = await bot.wait_for('message', timeout=120)
                if(msg.author == self.ctx.author):
                    if await self.endConvo(msg.content) == False:
                        await self.resp(msg.content)
                    else: return False
            except Exception:
                await self.ctx.send("Timed out. Please try again.")
                await self.endConvo("stop")
                break