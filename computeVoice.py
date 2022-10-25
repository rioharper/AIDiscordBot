import time
import discord
import os
from jsonfunk import *
import contextlib
import wave
import asyncio
from discord import FFmpegPCMAudio
from ctts import cTTS
import computeMessages

args = setconfig()


'''an extention of the class AI that will listen and play audio'''
class aud(computeMessages.ai):
        def __init__(self, engine, ctx, voice):
            super().__init__(engine, ctx)
            self.voice = voice
            self.sink = discord.sinks.RecSink()
            print("Initial")

        async def savefile(self, sink, *args):
            try:
                with open("transcription.txt", 'r') as f: result = f.read()
                print("User Said: " + result)
                os.remove("transcription.txt")
                if result != "" and await self.endConvo(result) == False:
                    await self.ctx.send("User: " + result)
                    await self.vcresp(result)
                else: return
            except FileNotFoundError:
                pass

        async def record(self):
            print('recording')
            self.voice.start_recording(
                self.sink,
                self.savefile,
                self.ctx.channel,
            )

        '''gets the duration of the audio file generated in vcresp, 
        used to stop the recording function to not listen when speaking to minimize false interactions'''
        def getdur(self, file):
            with contextlib.closing(wave.open(file,'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = round(frames / float(rate), 4)
                return duration

        async def vcsynth(self, input, voice):
            vfile = "talk" + str(time.strftime("%Y%m%d-%H%M%S")) + ".wav"
            try:
                cTTS.synthesizeToFile(vfile, input)
            except:
                print("Error Generating Voice! Is the TTS server online?")
            player = voice.play(FFmpegPCMAudio(vfile)) #play audio file on discord
            await asyncio.sleep(self.getdur(vfile))
            os.remove(vfile)
            

        async def vcresp(self, input): 
            responce = await self.resp(input)
            await self.vcsynth(responce, self.voice)
