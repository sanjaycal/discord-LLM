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
    speaker = "Cindy Baggins"

class systemMessage(message):
    speaker = "System"

class webScraperMessage(message):
    speaker = "Function Runner"

class networkMessage(message):
    speaker = "Network"

class requestMessage(message):
    speaker = "Request"

def basePrompt():
    with open("prompts/base","r") as f:
        return systemMessage(f.read())

def networkPrompt():
    with open("prompts/networkScraper","r") as f:
        return systemMessage(f.read())