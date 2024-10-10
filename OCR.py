from google.cloud import vision
import os
import time
import json
import datetime



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
        
def process_single_image(image_path: str, api_key: str) -> dict:
    """Process a single image and return the result."""
    result = {}
    try:
        start_time = time.time()
        text = detect_text(image_path, api_key)
        end_time = time.time()
        process_time = end_time - start_time
        
        result[os.path.basename(image_path)] = {
            'text': text,
            'process_time': process_time
        }
    except Exception as e:
        result[os.path.basename(image_path)] = {
            'text': f"Error: {str(e)}",
            'process_time': 0
        }

    return result, process_time

def process_directory(directory: str, api_key: str) -> dict:
    """Process all images in a directory and return a dictionary of results."""
    results = {}
    total_time = 0
    processed_files_path = os.path.join(directory, 'processed_files.json')

    # Load the list of previously processed files
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as f:
            processed_files = json.load(f)
    else:
        processed_files = {}

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            file_path = os.path.join(directory, filename)
            file_mtime = os.path.getmtime(file_path)

            # Check if the file is new or modified
            if filename not in processed_files or file_mtime > processed_files[filename]:
                # Use the process_single_image function to handle text detection
                try:
                    result = process_single_image(file_path, api_key)
                    results.update(result)  # Update results with the new data
                    total_time += result[os.path.basename(file_path)]['process_time']  # Add process time
                    # Update the processed files list
                    processed_files[filename] = file_mtime
                except Exception as e:
                    print(f"Error processing file {filename}: {str(e)}")  # Improved error handling
            else:
                # File has been processed before, skip it
                pass

    # Save the updated list of processed files
    with open(processed_files_path, 'w') as f:
        json.dump(processed_files, f)

    # Delete OCRed files that are no longer in the directory
    for processed_file in list(processed_files.keys()):
        if processed_file not in os.listdir(directory):
            del processed_files[processed_file]
            print(f"Removed tracking for deleted file: {processed_file}")

    return results, total_time


def inference(image_directory: str, api_key: str) -> str:
    """
    Process all images in a directory and return a string with all detected results.
    """
    results, total_process_time = process_directory(image_directory, api_key)

    if not results:
        return None

    output = []
    for filename, data in results.items():
        output.append(f"File: {filename}")
        output.append(f"Extracted text:\n{data['text']}")
        output.append("-" * 50)  # Add a separator between files

    return "\n".join(output)

def inference_single_image(image_path: str, api_key: str) -> str:
    """
    Process a single image and return a string with the detected result.
    """
    result, _ = process_single_image(image_path, api_key)  # Unpack the result properly

    if not result:
        return None

    output = []
    for filename, data in result.items():
        output.append(f"File: {filename}")
        output.append(f"Extracted text:\n{data['text']}")
        output.append("-" * 50)  # Add a separator between files

    # Write the output to a file instead of the result dictionary
    with open('single_result.txt', 'w') as f:
        f.write("\n".join(output))  # Write the formatted output string

    print(f"Current results written to single_result.txt")

    return "\n".join(output)


def main():
    # Get the API key from an environment variable
    api_key = os.environ.get('GOOGLE_CLOUD_API_KEY')
    if not api_key:
        print("Error: GOOGLE_CLOUD_API_KEY not set.")
        return

    # Specify the directory containing the images
    image_directory = 'images'

    print("Monitoring directory for new images. Press Ctrl+C to stop.")

    try:
        while True:
            # Use the inference function
            # @Xianhao could inference only when new images are detected or receive screenshot signal from Quest3
            result_string = inference(image_directory, api_key)
            
            if result_string:
                print("\nNew or modified files detected:")

                # Write to single_result.txt
                with open('single_result.txt', 'w') as f:
                    f.write(result_string)
                print(f"Current results written to single_result.txt")

                # Append to all_results.txt with timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open('all_results.txt', 'a') as f:
                    f.write(f"\n\n--- Results from {timestamp} ---\n\n")
                    f.write(result_string)
                print(f"Results appended to all_results.txt")

                # Send result_string to prompt.py for processing
                # brainstorming_result = process_input(result_string)
                # print("\nBrainstorming results:")
                # print(brainstorming_result)

            else:
                print("No new files detected. Checking again...", end="\r")  # Improved progress indicator

            time.sleep(1)  # Wait for 1 second before checking again

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
