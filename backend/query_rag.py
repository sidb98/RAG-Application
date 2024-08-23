import os
from .load_embedding import get_embedding_function
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
If there is no answer, write "No answer found."
"""


def query_rag(query_text: str):
    embedding = get_embedding_function()
    db = Chroma(persist_directory="./chroma_db", embedding_function=embedding)

    OPEN_AI_KEY = os.environ.get("OPEN_AI_KEY")
    chatgpt = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=OPEN_AI_KEY)

    search_result = db.similarity_search(query_text, k=3)

    context_text = "\n\n---\n\n".join([doc.page_content for doc in search_result])

    print(context_text)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # model = Ollama(model="mistral")
    # response_text = model.invoke(prompt)
    response_text = chatgpt(prompt)

    sources = [doc.metadata.get("id", None) for doc in search_result]
    if response_text.content == "No answer found.":
        sources = ["No sources found."]

    formatted_response = {
        "response_text": response_text.content,
        "sources": sources,
    }
    print(formatted_response)
    return formatted_response
