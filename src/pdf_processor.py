import hashlib
import logging
import time
from typing import Dict, Optional
from uuid import uuid4
from image_analyzer import ImageAnalyzer, ImageData, ModelAnalyzer
from pdf_file import PDFFile
from pdf_parser import extract_text_and_images
from vector_db import add_to_vector_db, initialize_vector_db

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, 
                 pdf_path: str,
                 model_analyzer: ModelAnalyzer,
                 vector_db_client = None):
        self.pdf_path = pdf_path
        self.image_analyzer = ImageAnalyzer(model_analyzer=model_analyzer)
        self.vector_db_client = vector_db_client or initialize_vector_db()

    def generate_file_identity(self) -> PDFFile:
        with open(self.pdf_path, 'rb') as f:
            content = f.read()
            content_hash = hashlib.sha256(content).hexdigest()
            
        return PDFFile(
            path=self.pdf_path,
            content_hash=content_hash,
            uuid=str(uuid4()),
            original_name=self.pdf_path,
            upload_timestamp=time.time()
        )

    def _store_file_metadata(self, file_identity: PDFFile) -> None:
        metadata_collection = self.vector_db_client.get_or_create_collection("pdf_files_metadata")
        metadata = {
            "uuid": file_identity.uuid,
            "content_hash": file_identity.content_hash,
            "original_name": file_identity.original_name,
            "upload_timestamp": file_identity.upload_timestamp
        }
        metadata_collection.add(
            ids=[file_identity.uuid],
            documents=[file_identity.original_name],  # Using filename as the document text
            metadatas=[metadata]
        )

    def is_duplicate_content(self, content_hash: str) -> tuple[bool, Optional[str]]:
        try:
            metadata_collection = self.vector_db_client.get_or_create_collection("pdf_files_metadata")
            all_files = metadata_collection.get()
            for metadata, id in zip(all_files["metadatas"], all_files["ids"]):
                if metadata.get("content_hash") == content_hash:
                    return True, metadata.get("uuid")
            return False, None
        except Exception:
            return False, None


    def process_content_item(self, content_item: Dict) -> str:
        if content_item['type'] == 'image':
            return self._process_image(content_item)
        elif content_item['type'] == 'text':
            return content_item['data']
        return ""

    def _process_image(self, content_item: Dict) -> str:
        image_data = ImageData(
            image=content_item['image'],
            ext=content_item['ext']
        )
        image_description = self.image_analyzer.describe_image(image_data)
        return f"##Image Description: {image_description.get('description', '')}" if image_description else ""

    def process_pdf(self) -> Dict:
        try:
            file_identity = self.generate_file_identity()
            
            is_duplicate, original_uuid = self.is_duplicate_content(file_identity.content_hash)
            if is_duplicate and original_uuid:
                return {
                    "status": "duplicate",
                    "message": "This PDF content has already been processed",
                    "file_uuid": original_uuid  # Return the original file's UUID
                }

            collection_name = f"pdf_{file_identity.uuid}"
            print("[collection_name] ", collection_name)
            content = extract_text_and_images(str(self.pdf_path))
            # print("[content] ", content)
            if not content:
                raise ValueError("No content extracted from PDF")

            processed_content = []
            for page in content:
                processed_text = self._process_page(page)
                processed_content.append({
                    "text": processed_text,
                    "page_number": page.get("page_number"),
                    "file_uuid": file_identity.uuid
                })

            self._store_file_metadata(file_identity)
            collection = add_to_vector_db(
                self.vector_db_client, 
                collection_name, 
                processed_content
            )
            
            return {
                "status": "success",
                "message": "Content processed successfully",
                "file_uuid": file_identity.uuid
            }

        except Exception as e:
            logger.error("Error processing PDF: %s", str(e), exc_info=True)
            return {"status": "error", "message": str(e)}

    def _process_page(self, page: Dict) -> str:
        processed_text = ""
        page_content = page.get("content", [])
        
        for content_item in page_content:
            text_data = self.process_content_item(content_item)
            processed_text += text_data + "\n"
            
        return processed_text
