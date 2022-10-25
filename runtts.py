import os
from jsonfunk import setconfig

args = setconfig()

command = ("tts-server --model_path " + args["voice"]["vcfilepath"] + " --config_path " + args["voice"]["vcconfigpath"])

os.system(command)
