import requests
import json
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)


def run_job(job_id: str, params: dict = None):
    """
    Trigger a Databricks job via REST API.
    Returns the raw response JSON.
    """
    try:
        url = f"{Config.DATABRICKS_HOST}/api/2.1/jobs/run-now"
        headers = {"Authorization": f"Bearer {Config.DATABRICKS_TOKEN}"}
        payload = {"job_id": job_id}

        if params:
            payload["notebook_params"] = params

        logger.info(f"Triggering Databricks job_id={job_id} with params={params}")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        logger.info(f"Databricks job triggered successfully: {response.json()}")
        return response.json()
    except Exception as e:
        logger.error(f"Databricks job execution failed: {e}", exc_info=True)
        raise


def retrieve_context(embedding: list, top_k: int = 3):
    """
    Calls a Databricks job that runs semantic search on stored vectors.
    Returns retrieved documents/context.
    """
    try:
        params = {
            "embedding": json.dumps(embedding),
            "top_k": str(top_k)
        }
        job_id = Config.DATABRICKS_JOB_ID

        logger.info(f"Retrieving context from Databricks (job_id={job_id}, top_k={top_k})")
        result = run_job(job_id, params)

        docs = result.get("documents", [])
        logger.info(f"Retrieved {len(docs)} documents from Databricks")
        return docs
    except Exception as e:
        logger.error(f"Context retrieval from Databricks failed: {e}", exc_info=True)
        raise
