import json

from langchain.llms import Ollama

import messagesLib

with open("config.json","r") as f:
    config = json.load(f)

model = Ollama(base_url='http://localhost:11434',model=config["model"])


def generateText(conversationAsString):
    output = model.invoke(conversationAsString)
    return messagesLib.botMessage(output)
