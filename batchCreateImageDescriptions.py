import os
import base64
from openai import OpenAI
from pathlib import Path
import numpy as np

# Set your API key here
OpenAI.api_key = '<YOUR_OPENAI_API_KEY>'

# Initialize the OpenAI client
client = OpenAI()


def encode_image_to_base64(image_path):
    """
    Encodes an image to base64.
    Args:
    - image_path (str): The path to the image file.
    Returns:
    - str: The base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def process_images(directory):
    """
    Processes each .jpg image in the specified directory by sending it to the OpenAI API
    and stores the responses in a text file.
    Args:
    - directory (str): The path to the directory containing the images.
    """
    # Ensure the output file is empty before starting
    with open("image_descriptions.txt", "w") as output_file:
        pass

    arrayOfFilenamesAndDescriptions = []  # Initialize the array to store filenames and descriptions

    # Iterate through all .jpg files in the directory
    for image_file in Path(directory).glob("*.jpg"):
        print(f"Processing {image_file.name}...")

        # Encode the image to base64
        base64_image = encode_image_to_base64(image_file)

        try:
            # Send the request to the OpenAI API
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What's in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                        ]
                    }
                ],
                max_tokens=300,
            )

            # Extract the response
            description = response.choices[0].message.content

            # Store the response in a text file
            with open("image_descriptions.txt", "a") as output_file:
                print(f"{image_file}: {description}", file=output_file)

            # Append filenames and descriptions to the 2D array
            arrayOfFilenamesAndDescriptions.append([image_file.name, description])

        except Exception as e:
            print(f"Error processing {image_file.name}: {e}")

    # create a numpy array which can be saved to disc for later usage
    np_array = np.array(arrayOfFilenamesAndDescriptions, dtype=object)

    # Save the NumPy array to an `.npy` file
    np.save('filenames_and_descriptions.npy', np_array)

    print("Saved filenames and descriptions to an npy file.")


if __name__ == "__main__":
    process_images('.')