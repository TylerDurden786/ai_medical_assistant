# Importing libraries
import os

# Getting Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Step2: Convert image to required format
import base64

# Path of reference file
image_path = "acne.jpg"


def encode_image(image_path):
    """
    Convert an image to base64 format
    Args:
        image_path (str): Path to the image file
    Returns:
        str: base64 encoded image
    """
    # Convert image to base64 format
    image_file = open(image_path, "rb")
    # Use utf-8 for decoding
    return base64.b64encode(image_file.read()).decode('utf-8')


# Step3: Setup Multimodal LLM
from groq import Groq

# Specify query details
query = "Is there something wrong with my face?"

# Specify type of model
model_type = "llama-3.2-90b-vision-preview"


def analyze_image_with_query(query, model, encoded_image):
    """
    Analyze an image with a given query using a multimodal language model.

    Args:
        query (str): The query to ask the model
        model (str): The type of model to use
        encoded_image (str): The base64 encoded image

    Returns:
        str: The response from the model
    """
    client = Groq()
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content
