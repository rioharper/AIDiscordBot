import json
import os
import yaml

#personalitiesjson = "personalities.json"
enginejson = "engines.json"

def delfiles(directory, ext): #delete any straggler files from current directory
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(ext)]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

def checkForFiles(directory):
    try: os.remove(directory + "dur.txt") 
    except : pass
    try: delfiles(directory, ".wav")
    except : pass
    try: delfiles(directory, ".ogg")
    except : pass


def setconfig():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)    

# def getNames(): #return names of all currently saved prompts
#     names = []
#     with open(personalitiesjson) as json_file:
#         data = json.load(json_file)
#         for name in data:
#             names.append(name['name'])
#     return names

# def getPrompt(pname): #returns the prompt of a specific prompt
#     with open(personalitiesjson) as json_file:
#             data = json.load(json_file)
#             for name in data:
#                 if(name['name'] == pname):
#                     return name['prompt']
#             print("prompt not found")

# def addpromptJson(name, prompt, createdby): #adds a new prompt to the json file
#     new = {"created by": createdby,    
#        "name": name, 
#        "prompt": prompt
#        }
#     with open(personalitiesjson, "r+") as json_file:
#         data = json.load(json_file)
#         data.append(new)
#         json_file.seek(0)
#         json.dump(data, json_file, indent=4)

# def removePrompt(name): #removes a prompt from the json file
#     with open(personalitiesjson, "r") as json_file:
#         data = json.load(json_file)
#     counter = 0
#     for personlity in data:
#         if(personlity['name'] == name):
#             data.pop(counter)
#             print("removed")
#             break
#         counter += 1
#     with open(personalitiesjson, 'w') as data_file:
#         json.dump(data, data_file, indent=4)    
 
def getEngines(): #returns the names of all currently saved engines
    engines = []
    with open(enginejson) as json_file:
        data = json.load(json_file)
        for engine in data:
            engines.append(engine['name'])
    return engines

def getEngine(name): #returns a specific engine from a name
    with open(enginejson) as json_file:
            data = json.load(json_file)
            for engine in data:
                if(engine['name'] == name):
                    return engine['engine']

def addEngine(name, engine, createdby): #adds a new engine to the json file
    new = {"created by": createdby,
         "name": name,
         "engine": engine} #create new engine
    with open(enginejson, "r+") as json_file:
        data = json.load(json_file)
        data.append(new)
        json_file.seek(0)
        json.dump(data, json_file, indent=4) #loads engine into engines.json file

def removeEngine(name): #removes an engine from the json file
    with open(enginejson, "r") as json_file:
        data = json.load(json_file)
    counter = 0
    for engine in data:
        if(engine['name'] == name):
            data.pop(counter)
            print("removed")
            break
        counter += 1
    with open('engines.json', 'w') as data_file:
        json.dump(data, data_file, indent=4)
