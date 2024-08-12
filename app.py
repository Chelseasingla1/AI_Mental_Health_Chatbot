from flask import Flask, render_template, request
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize Flask app
app = Flask(__name__)

# Initialize the chatbot model
model = OllamaLLM(model="llama3")
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Home route to display the chat interface
@app.route("/", methods=["GET", "POST"])
def home():
    context = ""
    if request.method == "POST":
        user_input = request.form["message"]
        context = request.form["context"]
        
        # Get the chatbot response
        result = chain.run({"context": context, "question": user_input})
        
        # Update context with user and AI conversation
        context += f"\nUser: {user_input}\nAI: {result}"
        return render_template("index.html", user_input=user_input, result=result, context=context)
    return render_template("index.html", context=context)

if __name__ == "__main__":
    app.run(debug=True)
