from google.cloud import vision
import os
import time


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
    total_time = 0
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            file_path = os.path.join(directory, filename)
            try:
                start_time = time.time()
                text = detect_text(file_path, api_key)
                end_time = time.time()
                process_time = end_time - start_time
                total_time += process_time
                results[filename] = {
                    'text': text,
                    'process_time': process_time
                }
            except Exception as e:
                results[filename] = {
                    'text': f"Error: {str(e)}",
                    'process_time': 0
                }
    return results, total_time


def inference(image_directory: str, api_key: str) -> str:
    """
    Process all images in a directory and return a string with all detected results.
    """
    results, total_process_time = process_directory(image_directory, api_key)

    output = []
    for filename, data in results.items():
        output.append(f"File: {filename}")
        output.append(f"Extracted text:\n{data['text']}")
        output.append(f"Process time: {data['process_time']:.2f} seconds")
        output.append("-" * 50)

    output.append(f"Total OCR process time: {total_process_time:.2f} seconds")

    return "\n".join(output)


def main():
    # Get the API key from an environment variable
    # os.environ.get('GOOGLE_CLOUD_API_KEY')
    api_key = "AIzaSyD_HTxDrvB0L4r5c2OF80XRRehMTJ0ab9w"  # TODO: change to env variable
    if not api_key:
        print("Error: GOOGLE_CLOUD_API_KEY not set.")
        return

    # Specify the directory containing the images
    image_directory = 'images'

    # Use the inference function
    result_string = inference(image_directory, api_key)
    print(result_string)


if __name__ == "__main__":
    main()
