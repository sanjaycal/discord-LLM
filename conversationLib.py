import json
import random

import messagesLib
import AIWrapper
import internetScraperLib

with open("config.json","r") as f:
    config = json.load(f)

class conversation:

    def __init__(self,messages = [], id=-1):
        self.messages = []
        self.id = 0
        if messages == []:
            messages.append(messagesLib.basePrompt())
        self.messages = messages
        self.id = id
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
        with open("conversations/" + str(self.id),"w") as f:
            self.saveToFile(f)
        aiOutput = self.messages[-1].content
        if ";;;" in aiOutput[:4]:
            self.messages.append(messagesLib.internetMessage(internetScraperLib.get_text(aiOutput.split(";;;")[-1].split("\n")[0])))
            aiOutput = self.generateAIResponse()
        return self.messages[-1].content
    
    def setSystemMessage(self,content):
        if len(self.messages)==0:
            self.messages.append(messagesLib.systemMessage(content))
        else:
            self.messages[0] = messagesLib.systemMessage(content)

    def setHumanResponse(self,content,user="User"):
        self.messages.append(messagesLib.humanMessage(content,user))

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
    out = conversation(messages,id = int(fp.name.split("conversations/")[-1]))
    return out
        