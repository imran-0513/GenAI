from flask import Flask, request, render_template
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize conversation history
conversation_history = []

@app.route('/')
def index():
    return render_template('index1.html', conversation_history=conversation_history)

@app.route('/generate_text', methods=['POST'])
def generate_text():
    user_input = request.form['user_input']

    # Update conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Use the correct endpoint for chat models
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            *conversation_history  # Include user input history
        ]
    )

    result = response['choices'][0]['message']['content']
    
    # Update conversation history with AI response
    conversation_history.append({"role": "assistant", "content": result})

    return render_template('index1.html', conversation_history=conversation_history)

if __name__ == '__main__':
    app.run(debug=True)
