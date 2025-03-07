from typing import Dict, List
from vector_db import initialize_vector_db, query_vector_db
import logging

logger = logging.getLogger(__name__)


class PDFQueryEngine:
    def __init__(self):
        self.vector_db_client = initialize_vector_db()

    def list_available_files(self) -> List[Dict]:
        metadata_collection = self.vector_db_client.get_collection("pdf_files_metadata")
        result = metadata_collection.get()
        return [
            {
                "id": id,
                "metadata": metadata
            }
            for id, metadata in zip(result["ids"], result["metadatas"])
        ]
    def query_by_file_uuid(self, file_uuid: str, query_text: str) -> Dict:
        try:
            collection = self.vector_db_client.get_collection(f"pdf_{file_uuid}")
            results = query_vector_db(collection, query_text)
            return {
                "status": "success",
                "results": results
            }
        except Exception as e:
            logger.error("Error querying database: %s", str(e), exc_info=True)
            return {"status": "error", "message": str(e)}
