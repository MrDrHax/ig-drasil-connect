def parseDocumentedQuestion(originalPrompt: str, documents: dict) -> str:
    toReturn = f"### The costumer asked: \n{originalPrompt} \n\n### Additional information \n"

    for bundle in documents['documents']:
        for doc in bundle:
            toReturn += f"- {doc}\n"

    return toReturn
