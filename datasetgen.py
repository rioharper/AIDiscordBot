from http import client
import numpy as np
import json
import random
import os
import asyncio
import openai

with open("questions.csv") as questions_file:
    questions = np.loadtxt(questions_file, dtype=str, delimiter=">")

# with open("prompts.csv") as prompts_file:
#     prompts = np.loadtxt(prompts_file, dtype=str, delimiter="|")

class dataset():
    async def __init__(self, filename, ctx):
        self.ctx = ctx
        self.filename = filename + ".json"
        self.counter = 0
        if os.path.exists(self.filename): self.getCount(), print("You have already generated: " + str(self.counter))
        else: self.createFile()
        self.question = ""
        self.answer = ""

    def getCount(self):
        with open(self.filename, 'r') as file:
            file_data = json.load(file)
            for entry in file_data:
                self.counter += 1
        return self.counter

    def createFile(self):
        with open(self.filename, 'w') as file:
            create = []
            json.dump(create, file, indent = 4)
    
    def dumpData(self):
        with open(self.filename,'r+') as file:
            file_data = json.load(file)
            file_data.append(self.entry)
            file.seek(0)
            json.dump(file_data, file, indent = 4, ensure_ascii=False)

    def checkdup(self):
        with open(self.filename, 'r') as json_file:
            json_data = json.load(json_file)
            for entry in json_data:
                if(entry["question"] == self.question):
                    return True
            return False

    def sendCount(self):
        return self.counter

    async def waitforinput(self, bot):
        while(True):
            try:
                msg = await bot.wait_for('message')
                print(msg.content)
                if(msg.author == self.ctx.author):
                    content = msg.content
                    return content
            except: return
            


class question(dataset):
    def __init__(self, filename, ctx):
        self.ctx = ctx
        self.filename = filename + ".json"
        self.counter = 0
        if os.path.exists(self.filename): self.getCount(), print("You have already generated: " + str(self.counter))
        else: self.createFile()
        self.question = ""
        self.answer = ""

    async def get_question(self):
        q1 = random.choice(questions)
        q2 = random.choice(questions)
        q3 = random.choice(questions)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt="Generate questions to get to know a person:\n" + q1 + "\n" + q2 + "\n" + q3 + "\n",
            temperature=1,
            max_tokens=20,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n", "?"]
        )
        resp = str(response.choices[0]['text'])
        print("Question: " + resp)
        return resp.strip() + "?"
    
    async def writetofile(self):
        if(self.answer == "skip"):
            await self.ctx.send("Skipping")
            return
        self.entry = {
            "prompt": self.question + "\nAI: ",
            "completion": str(self.answer) + "\n",
            "question": self.question
        }
        self.dumpData()

    async def get_answer(self, bot):
        async with self.ctx.typing():
            try:
                self.question = await self.get_question()
            except: await self.ctx.send("Whoops! OpenAI is acting funky. Try again in a minute.")
        # while(True):
        #     if self.checkdup() == True:
        #         await self.get_question()
        #     else: break
        await self.ctx.send("\nQuestion: " + self.question)
        self.answer = await self.waitforinput(bot)
        if self.answer != "stop":
            await self.writetofile()
        return self.answer

class prompt(dataset):
    def __init__(self, filename, ctx):
        self.ctx = ctx
        self.filename = filename + ".json"
        self.counter = 0
        if os.path.exists(self.filename): self.getCount(), print("You have already generated: " + str(self.counter))
        else: self.createFile()
        self.question = ""
        self.answer = ""
    
    def get_prompt(self):
        self.prompt = random.choice(prompts)
        self.question = self.prompt[1]
        self.context = self.prompt[0]

    async def writetofile(self):
        if(self.answer == "skip"):
            await self.ctx.send("Skipping")
            return
        self.entry = {
            "prompt": self.question + "\nAI:",
            "completion": " " + str(self.answer) + "\n",
            "question": self.question
        }
        self.dumpData()
    
    async def get_answer(self, bot):
        self.get_prompt()
        while(self.checkdup()):
            self.get_prompt()
        await self.ctx.send("\nYou are speaking " + self.context)
        await self.ctx.send("Person: " + self.question)
        self.answer = await self.waitforinput(bot)
        if self.answer != "stop":
            await self.writetofile()
        return self.answer