import conversationLib


convo = conversationLib.conversation()

while True:
    a = input(">>>")
    convo.setHumanResponse(a)
    AIResponse = convo.generateAIResponse()
    print(AIResponse)