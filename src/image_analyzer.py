from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional
import base64
from dotenv import load_dotenv
import os
from utils import parse_json_output

load_dotenv()

@dataclass
class ImageData:
    """Data structure for image information"""
    image: bytes
    ext: str

class ModelAnalyzer(ABC):
    """Base class for different AI model implementations"""
    
    @abstractmethod
    def analyze(self, image_data: ImageData) -> Dict[str, str]:
        """Analyze image using specific model implementation
        
        Args:
            image_data: ImageData object containing image bytes and extension
        Returns:
            Dictionary containing image description
        """
        pass

    @staticmethod
    def _encode_image_bytes(image_bytes: bytes) -> str:
        """Encode raw image bytes to base64
        
        Args:
            image_bytes: Raw binary image data
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(image_bytes).decode('utf-8')

class MistralAnalyzer(ModelAnalyzer):
    """Mistral AI specific implementation"""
    
    DEFAULT_MODEL = "pixtral-12b-2409"
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """Initialize Mistral analyzer
        
        Args:
            model: The Mistral model identifier to use
        Raises:
            ValueError: If MISTRAL_API_KEY environment variable is not set
        """
        from mistralai import Mistral
        self.model = model
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable must be set")
        self.client = Mistral(api_key=self.api_key)

    def analyze(self, image_data: ImageData) -> Dict[str, str]:
        """Analyze image using Mistral AI
        
        Args:
            image_data: ImageData object
        Returns:
            Dictionary with analysis results
        """
        message_prompt = self._build_prompt_message(image_data)
        response = self.client.chat.complete(
            model=self.model,
            messages=message_prompt
        )
        result = response.choices[0].message.content
        return parse_json_output(result)

    def _build_prompt_message(self, image_data: ImageData) -> List[Dict]:
        """Build the message prompt for Mistral AI
        
        Args:
            image_data: ImageData object
        Returns:
            List of message dictionaries for the API
        """
        base64_image = self._encode_image_bytes(image_data.image)
        image_url = f"data:image/{image_data.ext};base64,{base64_image}"

        return [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Task: Analyze the provided image and output a valid JSON object with one field:\n\n"
                        "\"description\": A detailed description of the image.\n"
                        "Example output:\n"
                        '{"description": "<detailed description>"}'
                    )
                },
                {
                    "type": "image_url",
                    "image_url": image_url
                }
            ]
        }]

class OpenAIAnalyzer(ModelAnalyzer):
    """OpenAI specific implementation"""
    
    def __init__(self):
        """Initialize OpenAI analyzer"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")
        # Initialize OpenAI client here

    def analyze(self, image_data: ImageData) -> Dict[str, str]:
        """Analyze image using OpenAI
        
        Args:
            image_data: ImageData object
        Returns:
            Dictionary with analysis results
        """
        # Implement OpenAI specific analysis
        pass

class ImageAnalyzer:
    """Main image analysis coordinator"""
    
    def __init__(self, model_analyzer: ModelAnalyzer):
        """Initialize ImageAnalyzer with specific model implementation
        
        Args:
            model_analyzer: Implementation of ModelAnalyzer to use
        """
        self.model_analyzer = model_analyzer

    def describe_image(self, image_data: ImageData) -> Dict[str, str]:
        """Analyze and describe the provided image
        
        Args:
            image_data: ImageData object
        Returns:
            Dictionary containing image description
        """
        return self.model_analyzer.analyze(image_data)

def main():
    """Main function for testing the ImageAnalyzer"""
    from pdf_parser import extract_text_and_images

    pdf_path = "PDF-Files/investigating-monuments.pdf"
    extracted_content = extract_text_and_images(pdf_path)
    
    image_data = ImageData(
        image=extracted_content[0]['images'][1]['image'],
        ext=extracted_content[0]['images'][1]['ext']
    )
    
    # Example using Mistral
    mistral_analyzer = MistralAnalyzer()
    analyzer = ImageAnalyzer(model_analyzer=mistral_analyzer)
    result = analyzer.describe_image(image_data)
    print("Mistral Analysis:", result)
    
    # Example using OpenAI (when implemented)
    # openai_analyzer = OpenAIAnalyzer()
    # analyzer = ImageAnalyzer(model_analyzer=openai_analyzer)
    # result = analyzer.describe_image(image_data)
    # print("OpenAI Analysis:", result)

if __name__ == "__main__":
    main()
