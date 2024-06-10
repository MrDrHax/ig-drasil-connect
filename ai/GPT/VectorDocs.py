import chromadb
import os
import logging

logger = logging.getLogger(__name__)

client = chromadb.PersistentClient()
collection: chromadb.Collection = None

def load():
    global collection

    if any([x for x in client.list_collections() if x.name == "venue_data"]):
        logger.info("Database already loaded")

        collection = client.get_collection("venue_data")

        return
    
    collection = client.create_collection("venue_data")

    # Load the vector docs
    docs = []
    tags = []
    ids = []

    for doc in os.listdir("documents"):
        
        with open(f"documents/{doc}", "r") as f:
            i = 0
            for line in f.readlines():
                docs.append(line.strip('\n'))
                tags.append({"source": doc})
                ids.append(f"{doc}_{i}")

                i += 1

    collection.add(
        documents=docs,
        metadatas=tags,
        ids=ids
    )


def retrieve(prompt: str) -> dict:
    results = collection.query(
        query_texts=[prompt],
        n_results=5,
    )

    return results

load()

if __name__ == "__main__":
    print(retrieve("What venues are available for a concert?"))
    print(retrieve("What concert is avaible in CDMX?"))