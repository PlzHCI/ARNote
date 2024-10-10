import openai
import os

# 设置OpenAI API密钥
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_all_results():
    try:
        with open('all_results.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "File 'all_results.txt' not found."

def process_input(content):
    prompt = f"Please brainstorm based on the contents of the following documents:\n\n{content}\n\nCould you kindly provide some creative ideas?"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative assistant, skilled in brainstorming."},
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
    print("\nResults of the brainstorming session:")
    print(result)

if __name__ == "__main__":
    main()
