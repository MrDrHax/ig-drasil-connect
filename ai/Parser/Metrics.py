import json

def parseMetrics(json_data: dict) -> str:
    transcript = ''

    for chat in json_data['Transcript']:
        transcript += f"{chat['ParticipantId']}: ({chat['Sentiment']}) {chat['Content']}\n"

    transcript += f"END OF CHAT\n\n"

    transcript += f"Chat Duration: {json_data['ConversationCharacteristics']['TotalConversationDurationMillis']}\n"
    transcript += f"Interruptions: {json_data['ConversationCharacteristics']['Interruptions']['TotalCount']}\n"
    transcript += f"No talk time: {json_data['ConversationCharacteristics']['NonTalkTime']['TotalTimeMillis']}\n"
    transcript += f"Agent sentiment: {json_data['ConversationCharacteristics']['Sentiment']['OverallSentiment']['AGENT']}\n"
    transcript += f"Customer sentiment: {json_data['ConversationCharacteristics']['Sentiment']['OverallSentiment']['CUSTOMER']}\n"

    return transcript

if __name__ == "__main__":
    with open('testcall.json', 'r') as file:
        json_data = json.load(file)

    print(parseMetrics(json_data))