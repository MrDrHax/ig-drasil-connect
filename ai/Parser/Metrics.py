import json

def parseMetrics(json_data: dict) -> str:
    transcript = ''

    for chat in json_data['Transcript']:
        transcript += f"{chat['ParticipantId']}: ({chat['Sentiment']}) {chat['Content']}\n"

    transcript += f"END OF CHAT\n\n"

    try:
        transcript += f"Chat Duration: {json_data['ConversationCharacteristics']['TotalConversationDurationMillis']}\n"
    except KeyError:
        transcript += "Chat Duration: 0\n"
    try:
        transcript += f"Interruptions: {json_data['ConversationCharacteristics']['Interruptions']['TotalCount']}\n"
    except KeyError:
        transcript += "Interruptions: none\n"
    try:
        transcript += f"No talk time: {json_data['ConversationCharacteristics']['NonTalkTime']['TotalTimeMillis']}\n"
    except KeyError:
        transcript += "No talk time: 0\n"
    try:
        transcript += f"Agent sentiment: {json_data['ConversationCharacteristics']['Sentiment']['OverallSentiment']['AGENT']}\n"
    except KeyError:
        transcript += "Agent sentiment: positive\n"
    try:
        transcript += f"Customer sentiment: {json_data['ConversationCharacteristics']['Sentiment']['OverallSentiment']['CUSTOMER']}\n"
    except KeyError:
        transcript += "Customer sentiment: positive\n"

    return transcript

if __name__ == "__main__":
    with open('testcall.json', 'r') as file:
        json_data = json.load(file)

    print(parseMetrics(json_data))