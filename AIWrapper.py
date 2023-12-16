import json

from langchain.llms import Ollama
from requests import Session

import messagesLib


session = Session()

with open("config.json","r") as f:
    config = json.load(f)

model = Ollama(base_url='http://localhost:11434',model=config["model"])


def generateTextOld(conversationAsString):
    output = model.invoke(conversationAsString)
    return messagesLib.botMessage(output)



def generateText(conversationAsString):
    global session
    data_json = {"model":config["model"], "prompt":conversationAsString, "stream": False}
    r = session.post("http://localhost:11434/api/generate", data = json.dumps(data_json))
    output = json.loads(r.text)["response"]
    return messagesLib.botMessage(output)