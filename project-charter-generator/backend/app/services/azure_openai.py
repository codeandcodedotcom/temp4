import os
from openai import AzureOpenAI
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

client = AzureOpenAI(
    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
    api_key=Config.AZURE_OPENAI_KEY,
    api_version=Config.AZURE_API_VERSION
)

EMBEDDING_DEPLOYMENT = Config.AZURE_EMBEDDING_DEPLOYMENT
CHAT_DEPLOYMENT = Config.AZURE_CHAT_DEPLOYMENT   


def embed_text(text: str):
    """
    Create embeddings for input text using Azure OpenAI embedding model.
    """
    try:
        logger.info(f"Requesting embedding for input text (length={len(text)})")
        response = client.embeddings.create(
            model=EMBEDDING_DEPLOYMENT,
            input=text
        )
        embedding = response.data[0].embedding
        logger.info(f"Embedding generated successfully (length={len(embedding)})")
        return embedding
    except Exception as e:
        logger.error(f"Embedding generation failed: {str(e)}", exc_info=True)
        raise


def generate_answer(prompt: str):
    """
    Generate answer using Azure OpenAI chat model.
    """
    try:
        logger.info(f"Generating answer with prompt length={len(prompt)}")
        response = client.chat.completions.create(
            model=Config.AZURE_CHAT_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE
        )
        answer = response.choices[0].message.content
        logger.info(f"LLM response generated successfully (length={len(answer)})")
        return answer
    except Exception as e:
        logger.error("Answer generation failed: %s", str(e), exc_info=True)
        raise
