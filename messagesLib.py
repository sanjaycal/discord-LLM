import json

with open("config.json","r") as f:
    config = json.load(f)


class message:
    speaker = ""

    def __init__(self,message):
        self.content = message
    
    def __str__(self):
        return f"### {self.speaker}:\n{self.content}\n"


class humanMessage(message):
    def __init__(self,message,user="User"):
        self.content = message
        self.speaker = user


class botMessage(message):
    speaker = "Assistant"

class systemMessage(message):
    speaker = "System"

def basePrompt():
    with open("prompts/base","r") as f:
        return systemMessage(f.read())