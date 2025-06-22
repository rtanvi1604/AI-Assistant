import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, request, render_template

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def get_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        user_input = request.form['user_input']
        function_type = request.form['function']

        if function_type == "answer":
            prompt = f"Answer this question briefly: {user_input}"
        elif function_type == "summarize":
            prompt = f"Summarize the following text: {user_input}"
        elif function_type == "creative":
            prompt = f"Write creatively based on: {user_input}"
        else:
            prompt = user_input

        result = get_ai_response(prompt)

        feedback = request.form.get('feedback')
        if feedback:
            with open("feedback.txt", "a") as f:
                f.write(f"{feedback}\n")

    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)

