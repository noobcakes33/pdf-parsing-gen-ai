import fitz

def extract_text_and_images(pdf_path):
    """
    Extract text and images in their original page order, sorted by bbox positions.
    Returns a list of pages, each containing a sequence of "text" or "image" items.
    """
    doc = fitz.open(pdf_path)
    content = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_content = []
        
        # Get the page's layout in rendering order
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_IMAGES)["blocks"]
        
        # Sort blocks by their bbox (top-to-bottom, left-to-right)
        blocks_sorted = sorted(blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))  # Sort by y1, then x1
        
        for block in blocks_sorted:
            if block["type"] == 0:  # Text block
                # Extract text from all spans in the block
                text = "".join([span["text"] for line in block["lines"] for span in line["spans"]])
                if text.strip():  # Only add non-empty text
                    page_content.append({
                        "type": "text",
                        "data": text.strip()
                    })
                
            elif block["type"] == 1:  # Image block
                try:
                    # Extract image data
                    image_data = {
                        "type": "image",
                        "image": block["image"],
                        "ext": block["ext"]
                    }
                    page_content.append(image_data)
                except Exception as e:
                    print(f"Failed to extract image with xref {block['number']}: {e}")
                    print(block)
        
        # Add the page's content to the overall content list
        content.append({"page_number": page_num + 1, "content": page_content})
    
    return content


if __name__ == "__main__":
    pdf_path = "PDF-Files/investigating-monuments.pdf"
    extracted_content = extract_text_and_images(pdf_path)
    print(extracted_content[0]['images'][0]['image'])
    print(extracted_content[0]['images'][0]['ext'])