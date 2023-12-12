import json
import random
import copy

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
    
    def setSystemMessage(self,content):
        if len(self.messages)==0:
            self.messages.append(messagesLib.systemMessage(content))
        else:
            self.messages[0] = messagesLib.systemMessage(content)

    def setHumanResponse(self,content,user="User"):
        self.messages.append(messagesLib.humanMessage(content,user))
    
    def saveToFile(self,fp):
        saveString = ""
        for message in self.messages:
            saveString += str(message) + config["separation-character"]
        fp.write(saveString[:-len(config["separation-character"])])
    
    def getBillResponse(self, search_term):
        billmessages = []
        billmessages.append(messagesLib.networkPrompt())
        billmessages.append(messagesLib.requestMessage(search_term))
        billConvo = conversation(messages=billmessages)
        out = billConvo.generateAIResponse()
        self.messages.append(messagesLib.webScraperMessage(out))
        

    def generateAIResponse(self):
        self.messages.append(AIWrapper.generateText(str(self)))
        with open("conversations/" + str(self.id),"w") as f:
            self.saveToFile(f)
        aiOutput = self.messages[-1].content
        while aiOutput[0] == " ":
            aiOutput = aiOutput[1:]
        if "<" in aiOutput and "</" in aiOutput and ">" in aiOutput:
            print(aiOutput)
            functionToCall = json.loads(aiOutput.split(">")[1].split("</")[0])
            functionToCall["name"] = aiOutput.split(">")[0].split("<")[-1]
            match functionToCall["name"]:
                case "websearch":
                    self.getBillResponse(functionToCall["arguments"]["searchQuery"])
                case "googlesearch":
                    self.messages.append(messagesLib.networkMessage(str(internetScraperLib.google_search(functionToCall["arguments"]["searchQuery"],num=5))))
                case "crawlWebPage":
                    try:
                        self.messages.append(messagesLib.networkMessage(internetScraperLib.get_text(functionToCall["arguments"]["URL"])))
                    except:
                        self.messages.append(messagesLib.networkMessage(internetScraperLib.get_text(functionToCall["URL"])))
            aiOutput = self.generateAIResponse()
            while aiOutput[0] == " ":
                aiOutput = aiOutput[1:]
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
    out = conversation(messages,id = int(fp.name.split("conversations/")[-1]))
    return out
        