import re
import json5
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pdf_processor.log'),
            logging.StreamHandler()
        ]
    )

def parse_json_output(output_str):
    """
    Parses a string expected to be a JSON object.
    Removes markdown code fences and uses json5 to handle unescaped inner quotes.

    Args:
        output_str (str): The raw output string from the model.

    Returns:
        dict: The parsed JSON as a dictionary.

    Raises:
        ValueError: If the output cannot be parsed.
    """
    # Remove markdown code fences if present.
    cleaned = re.sub(r"^```(?:json)?\s*|```$", "", output_str.strip(), flags=re.DOTALL)
    cleaned = cleaned.replace("{'", '{"}').replace(", '", ', "').replace("':", '":')
    try:
        data = json5.loads(cleaned)
    except Exception as e:
        raise ValueError("Failed to parse JSON output: " + str(e))
    return data
