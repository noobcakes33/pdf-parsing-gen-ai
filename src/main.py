import logging
from pdf_query_engine import PDFQueryEngine
from image_analyzer import  MistralAnalyzer
from pdf_processor import PDFProcessor
from pprint import pprint
from utils import setup_logging


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    setup_logging()
    
    # pdf_path="PDF-Files/Robinson-Crusoe-in-Levels-PDF.pdf"
    pdf_path="PDF-Files/investigating-monuments.pdf"
    model_analyzer = MistralAnalyzer()
    processor = PDFProcessor(pdf_path=pdf_path, model_analyzer=model_analyzer)
    
    result = processor.process_pdf()
    file_uuid = result["file_uuid"]  # This will be the original UUID for duplicates
    
    query_engine = PDFQueryEngine()
    # query = "What did the man discover on the ship during the storm?"
    query = "What is a cenotaph?"
    query_result = query_engine.query_by_file_uuid(file_uuid, query)
    pprint(query_result)

    # available_files = query_engine.list_available_files()
    # print("Available files:\n")
    # pprint(available_files)
