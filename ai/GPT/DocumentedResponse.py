from GPT.VectorDocs import retrieve
from GPT.SessionManager import GPTManager
from Parser.DocumentData import parseDocumentedQuestion

def get_response(prompt: str, callID: str, model: GPTManager) -> str:
    data = retrieve(prompt)

    parsed = parseDocumentedQuestion(prompt, data)

    chatID = 'call-{callID}'

    try:
        response = model.prompt(chatID, parsed)
    except ValueError:
        model.create_session(chatID, """You are an agent in a call center. The costumer has just arrived and has a question. 
Your job is to make sure the costumer leaves satisfied with the information they need. However, you do not know much about the costumer's question or how to solve it.
Please ask the costumer for more information and try to solve their question. 
Every time the costumer makes a question, additional information about the question will be provided from documentation.
Beware! The costumer might not know the exact question to ask or might give you wrong information.
You must treat the costumer with respect and patience, be cheerful and understanding.
You may ask as many questions as you need to solve the costumer's question, but try to solve it as fast as possible so the costumer does not get frustrated.
You must always respond as if you are talking directly to the costumer.
""", 
                             "{0}\n\n### What should I tell the costumer?\n")
        
        response = model.prompt(chatID, parsed)

    return response