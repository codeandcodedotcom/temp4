from azure.storage.blob import BlobServiceClient
import io
from PyPDF2 import PdfReader

def read_pdfs_from_blob_sas(account_name: str, sas_token: str, container_name: str, blob_names: list):
    """
    Reads PDF files from Azure Blob Storage using SAS Token and extracts text.
    
    Args:
        account_name (str): Azure Storage account name.
        sas_token (str): Shared Access Signature (SAS) token.
        container_name (str): Container where PDFs are stored.
        blob_names (list): List of blob (file) names inside the container.
    
    Returns:
        dict: {blob_name: pdf_text}
    """
    # Build blob service client URL
    blob_service_url = f"https://{account_name}.blob.core.windows.net{sas_token}"
    blob_service_client = BlobServiceClient(account_url=blob_service_url)

    container_client = blob_service_client.get_container_client(container_name)

    pdf_texts = {}

    for blob_name in blob_names:
        blob_client = container_client.get_blob_client(blob_name)
        downloader = blob_client.download_blob()
        pdf_bytes = downloader.readall()

        # Extract text from PDF
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        
        pdf_texts[blob_name] = text

    return pdf_texts



pdf_texts = read_pdfs_from_blob_sas(
    account_name="mystorageaccount",
    sas_token="?sv=2025-09-04&ss=bfqt&srt=sco&sp=rl...",  # full SAS token including ?
    container_name="mycontainer",
    blob_names=["file1.pdf", "file2.pdf"]
)


# pip install azure-storage-blob PyPDF2