import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

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

# Streamlit UI
st.title("Mental Health Chatbot")

context = st.session_state.get("context", "")

user_input = st.text_area("You:", "")
if st.button("Send"):
    if user_input:
        # Get the chatbot response
        result = chain.run({"context": context, "question": user_input})
        context += f"\nUser: {user_input}\nAI: {result}"
        st.session_state["context"] = context
        
        st.markdown(f"**Bot:** {result}")

# Display the conversation history
st.text_area("Conversation History", value=context, height=300, disabled=True)
