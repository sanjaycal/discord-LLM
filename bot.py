import discord

import conversationLib


TOKEN = open("token","r").read()

intents = discord.Intents.default()

intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "?help":
        await message.reply("This an AI LLM that acts as a way for you to talk with an llm, use ?? followed by a message to get started, eg ```??Hello AI, what is your name?```, you can reply to the AI's message in discord with ?? at the start of your message to continue to conversation")
    
    if message.content[:2] == "??":
        if message.reference != None:
            convoID = (await message.channel.fetch_message(message.reference.message_id)).content.split("[")[-1][:-1]
            with open(convoID,"r") as f:
                convo = conversationLib.readConversationFromFile(f)
        else:
            convo = conversationLib.conversation()
            convo.setHumanResponse(message.content[2:])
        
        AIResponse = convo.generateAIResponse()

        replyMessage = f"{AIResponse}[{convo.id}]"

        await message.reply(replyMessage)

client.run(TOKEN)