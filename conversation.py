import json
import random

import messagesLib
import AIWrapper

with open("config.json","r") as f:
    config = json.load(f)

class conversation:
    messages = []
    id = 0

    def __init__(self,messages = [], id=-1):
        self.messages = messages
        if id == -1:
            self.id = random.randint(0,1000000000000000000000000000000000000000)
    
    def __str__(self):
        saveString = ""
        for message in self.messages:
            saveString += str(message)
        return saveString
    
    def saveToFile(self,fp):
        saveString = ""
        for message in self.messages:
            saveString += str(message) + config["separation-character"]
        fp.write(saveString[:-len(config["separation-character"])])
    
    def generateAIResponse(self):
        self.messages.append(AIWrapper.generateText(str(self)))
        with open(str(self.id),"w") as f:
            self.saveToFile(f)
        return self.messages[-1].content


def readConversationFromFile(fp):
    fileText = fp.read()
    messageStrs = fileText.split(config["separation-character"])
    messages = []
    for message in messageStrs:
        speaker = message.split("\n")[0][4:-1]
        messageContent = message.split("\n")[1:]
        a = ''
        for i in messageContent:
            a+=i
        messageContent = a
        if speaker == "System":
            messages.append(messagesLib.systemMessage(messageContent))
        elif speaker == "Assistant":
            messages.append(messagesLib.botMessage(messageContent))
        else:
            messages.append(messagesLib.humanMessage(messageContent,speaker))
    out = conversation(messages,id = int(fp.name))
    return out
        



convo = conversation()

convo.messages.append(messagesLib.systemMessage("You are Cindy Baggins, be nice"))

convo.messages.append(messagesLib.humanMessage("How Are You"))

with open(str(convo.id),"w") as f:
    convo.saveToFile(f)

with open(str(convo.id),"r") as f:
    convo2 = readConversationFromFile(f)


print(convo2.generateAIResponse())