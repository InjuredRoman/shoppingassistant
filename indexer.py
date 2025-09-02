import os
from dotenv import load_dotenv

# loads api keys present in `.env` file
load_dotenv()

apiKeys = [
    "GOOGLE_API_KEY",
]

catalogSrcUrls = (
    "https://www.nytimes.com/wirecutter/gifts/gifts-that-last-forever/",
)

def loadAPIKeysIntoEnvironment():
    keys = {}
    for apiKey in apiKeys:
        try:
            keys[apiKey] = os.getenv(apiKey)
            os.environ[apiKey] = os.getenv(apiKey)
        except:
            print(f"Can't find {apiKey} in environment variables. Double check it's defined in local `.env` file")
    return keys

## Thanks to this tutorial for the instruction: https://python.langchain.com/docs/tutorials/rag/

# catalog parsing, and langchain doc loader and text splitter import
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
# from langchain import hub
from langchain_core.prompts import PromptTemplate

# def loadChatModel(model="gemini-2.0-flash-lite", modelProvider="google_genai"):
def loadChatModel(model="gemini-2.5-flash", modelProvider="google_genai"):
    return init_chat_model(model, model_provider=modelProvider)

def loadEmbeddings(model="models/gemini-embedding-001"):
    return GoogleGenerativeAIEmbeddings(model=model)

def loadVectorStore(embeddings):
    return InMemoryVectorStore(embeddings)

def indexCatalog(catalogSourceUrls, verbosity=1, use_cache=True):
    if (use_cache):
        set_llm_cache(SQLiteCache(database_path=".langchain.db")) ## save some requests

    loader = WebBaseLoader(
        web_paths=catalogSourceUrls,
        # bs_kwargs=dict(
        #     parse_only= bs4.SoupStrainer(
        #         class_=("chapter-head", "chapter__head", "chapter-body", "chapter__body")
        #     )
        # ),
    )

    loadAPIKeysIntoEnvironment()
    llm = loadChatModel()
    embeddings = loadEmbeddings()
    vectorStore = loadVectorStore(embeddings)

    textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = loader.load()
    allSplits = textSplitter.split_documents(docs)
    if (verbosity > 0):
        print(f"Split given catalog(s) into {len(allSplits)} sub-documents.")

    vectorStore.add_documents(documents=allSplits)

    # adapted from: https://smith.langchain.com/hub/rlm/rag-prompt
    prompt = """
                You are an assistant, named Jeeves, for question-answering tasks
                and social support.
                Use user-supplied image(s) (if any) and the following pieces of
                retrieved context to answer the question, if it concerns shopping,
                and respond with kindness and emotional support to all inquiries (shopping-related or otherwise).
                If you don't know the answer, say so so as not to mislead the client.
                Remember, brevity is the soul of wit! Keep the answer concise.
                Also, as Jeeves, try and talk like a combination of Rosencrantz and
                Guildenstern.
            Question: {question}
            Images: {imageContent}
            Context: {context}
            Answer:"""

    prompt = PromptTemplate.from_template(prompt)


    return prompt, vectorStore, llm

class State(TypedDict):
    question: str
    imageContent: List[str]
    context: List[Document]
    answer: str

def main():
    prompt, vectorStore, llm = indexCatalog(catalogSrcUrls)

    def retrieve(state: State):
        retrievedDocs = vectorStore.similarity_search(state["question"])
        return {"context": retrievedDocs}

    def generate(state: State):
        docCont = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({
            "question": state["question"],
            "imageContent": state["imageContent"],
            "context": docCont,
            }
            )
        reply = llm.invoke(messages)
        return { "answer": reply.content }

    graphBuilder = StateGraph(State).add_sequence([retrieve, generate])
    graphBuilder.add_edge(START, "retrieve")
    graph = graphBuilder.compile()
    return graph

import base64
def serializeImage(im: str):
    with open(im, 'rb') as ifd:
        byteString = base64.b64encode(ifd.read()).decode()
        return byteString

if __name__=='__main__':
    g = main()
    reply = g.invoke(
        {
            "question": "What's a good gift for a guy that looks like this?",
            "imageContent": [ serializeImage(im) for im in ['./assets/marlon_in_coat.webp'] ]
        }
        )
    answer = reply["answer"]
    print(answer)