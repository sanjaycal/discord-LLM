import discord

import conversationLib


async def reply(message,text,convoID):
    n = 2000
    to_send = [text[i:i+n] for i in range(0, len(text), n)]
    if len(to_send[-1])<1500:
        to_send[-1]+=f"[{convoID}]"
    else:
        tmp = to_send[-1][1000:]
        to_send[-1] = to_send[-1][:1000]
        to_send.append(tmp + f"[{convoID}]")
    for m in to_send:
        await message.reply(m)

TOKEN = open("token","r").read()

intents = discord.Intents.default()

intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "?help":
        await message.reply("This an AI LLM that acts as a way for you to talk with an llm, use ?? followed by a message to get started, eg ```??Hello AI, what is your name?```, you can reply to the AI's message in discord with ?? at the start of your message to continue to conversation, my source code can be found at https://github.com/sanjaycal/discord-LLM")
    
    if message.content[:2] == "??":
        

        if message.reference != None:
            convoID = (await message.channel.fetch_message(message.reference.message_id)).content.split("[")[-1][:-1]
            with open("conversations/" + convoID,"r") as f:
                convo = conversationLib.readConversationFromFile(f)
        else:
            convo = conversationLib.conversation(messages=[])
        convo.setHumanResponse(message.content[2:],message.author)

        AIResponse = convo.generateAIResponse()

        await reply(message, str(AIResponse),convo.id)

client.run(TOKEN)