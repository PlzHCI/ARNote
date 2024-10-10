import openai
import os

# set up OpenAI API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
topic = "How to build a good collaboration team?"

def read_all_results():
    try:
        with open('single_result.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "File 'all_results.txt' not found."

def process_input(content):
    prompt = f"Please brainstorm based on the contents of the following documents:\n\n{content}\n\nCould you kindly provide some creative ideas? Keep every single idea less than 6 words.\
        No explanation is needed for each idea. At most 5 ideas are needed."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a creative assistant, skilled in brainstorming. The brainstorming topic is {topic}"},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content.strip()
        return result

    except Exception as e:
        return f"An error has occurred: {str(e)}"

def main():
    print("Currently reading all_results.txt and engaging in brainstorming...")
    content = read_all_results()
    result = process_input(content)

if __name__ == "__main__":
    main()
