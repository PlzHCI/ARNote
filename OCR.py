from google.cloud import vision
import os

# TODO: add object detection?


def detect_text(path: str, api_key: str) -> str:
    """Detects text in the file and returns the extracted text."""

    client = vision.ImageAnnotatorClient(
        client_options={"api_key": api_key}
    )

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(
                response.error.message)
        )

    # Join the texts together, with each paragraph separated by a new line
    paragraphs = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                paragraph_text = " ".join([
                    "".join([symbol.text for symbol in word.symbols])
                    for word in paragraph.words
                ])
                paragraphs.append(paragraph_text)

    return "\n".join(paragraphs)


def process_directory(directory: str, api_key: str) -> dict:
    """Process all images in a directory and return a dictionary of results."""
    # TODO: OCR if new file is detected, delete the OCRed file
    results = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            file_path = os.path.join(directory, filename)
            try:
                text = detect_text(file_path, api_key)
                results[filename] = text
            except Exception as e:
                results[filename] = f"Error: {str(e)}"
    return results


def main():
    # Get the API key from an environment variable
    # os.environ.get('GOOGLE_CLOUD_API_KEY')
    api_key = "api_key"  # TODO: change to env variable
    if not api_key:
        print("Error: GOOGLE_CLOUD_API_KEY not set.")
        return

    # Specify the directory containing the images
    image_directory = 'images'

    # Process the directory
    results = process_directory(image_directory, api_key)

    if isinstance(results, str):
        print(results)
    else:
        # Print the results
        for filename, text in results.items():
            print(f"File: {filename}")
            print(f"Extracted text:\n{text}\n")
            print("-" * 50)


if __name__ == "__main__":
    main()
