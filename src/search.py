import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def get_database_url() -> str:
    return os.getenv("DATABASE_URL")


def get_collection_name() -> str:
    return os.getenv("PG_VECTOR_COLLECTION_NAME")


def get_embeddings():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        model = os.getenv("OPENAI_EMBEDDING_MODEL")
        return OpenAIEmbeddings(model=model)

    # gemini_api_key = os.getenv("GOOGLE_API_KEY")
    # if gemini_api_key:
    #     model = os.getenv("GOOGLE_EMBEDDING_MODEL")
    #     return GoogleGenerativeAIEmbeddings(model=model)

    raise ValueError(
        "Env vars OPENAI_API_KEY ou GOOGLE_API_KEY devem ser definidas"
    )


def get_llm():
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-5-nano")

    if os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

    raise ValueError("Defina OPENAI_API_KEY ou GOOGLE_API_KEY no arquivo .env")


def get_vector_store() -> PGVector:
    return PGVector(
        embeddings=get_embeddings(),
        collection_name=get_collection_name(),
        connection=get_database_url(),
        use_jsonb=True,
    )


def search_prompt(question=None):
    try:
        vector_store = get_vector_store()
        llm = get_llm()
    except Exception as e:
        print(f"Erro ao inicializar o chat. Verifique os erros de inicialização: {e}")
        return None

    def reply(pergunta: str) -> str:
        # 10 chunks mais relevantes
        results = vector_store.similarity_search_with_score(pergunta, k=10)
        chunks = []
        for doc, _ in results:
            chunks.append(doc.page_content)
        contexto = "\n\n".join(chunks)
        prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)
        response = llm.invoke(prompt)
        return response.content.strip()

    if question is not None:
        return reply(question)
    return reply
