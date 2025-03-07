# PDF Parsing Gen AI

A powerful PDF processing system that combines text extraction, image analysis, and vector database storage for intelligent document querying.

## Features

- PDF content extraction (text and images)
- Image analysis using Mistral AI
- Vector database storage with ChromaDB
- Duplicate detection and handling
- Content querying

## Installation

1. Clone the repository:
```bash
git clone https://github.com/noobcakes33/pdf-parsing-gen-ai.git
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your PDF files in the `PDF-Files` directory

2. Process and query a PDF:

```python
# Initialize the Mistral model analyzer
model_analyzer = MistralAnalyzer()

# Set up the PDF processor with your file
pdf_path = "PDF-Files/your-document.pdf"
processor = PDFProcessor(pdf_path=pdf_path, model_analyzer=model_analyzer)

# Process the PDF
result = processor.process_pdf()

# Get the file UUID for querying
file_uuid = result["file_uuid"]

# Initialize query engine and perform queries
query_engine = PDFQueryEngine()
query = "Your question about the document content"
query_result = query_engine.query_by_file_uuid(file_uuid, query)

# Display results
pprint(query_result)
```

Example queries:
- "What is a cenotaph?"
- "What did the man discover on the ship during the storm?"

## Project Structure

```
pdf-parsing-gen-ai/
├── PDF-Files/               # Directory for PDF documents
├── chromadb/                # Vector database storage
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
└── src/                     # Source code directory
    ├── image_analyzer.py    # Image analysis implementation
    ├── __init__.py          # Python package initialization
    ├── main.py              # Main application entry point
    ├── pdf_file.py          # PDF file handling
    ├── pdf_parser.py        # PDF parsing implementation
    ├── pdf_processor.py     # PDF processing orchestration
    ├── pdf_query_engine.py  # Query system implementation
    ├── utils.py             # Utility functions
    └── vector_db.py         # Vector database operations

```