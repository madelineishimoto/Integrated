from openai import OpenAI
from langchain.chat_models import ChatOpenAI 
from decouple import config
from langchain.memory import ConversionBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st
import requests
import os 



#youtube
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=""""You are currently talking to a human? answer in friendly tone
    
    chat_history: {chat_history}
    
    Human: {question}"""
)

llm = ChatOpenAI(openai_api_key=config("OPEN_AI_KEY"))
memory = ConversionBufferWindowMemory(memory_key="chat_history", k=4)
llm_chain = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt
)
#youtube 

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
#MARKDOWN FROM STREAMLIT
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff; /* lighter blue */
    color: #ffffff;
    border-color: #0099ff;
}
div.stButton > button:hover {
    background-color: #0000ff; /*pure blue*/
    color: #ffffff;
    border-color: #0099ff;      
}
</style>
""", unsafe_allow_html=True)

#MARKDOWN FROM STREAMLIT

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
#streamlit widgets
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
    #REAL Python
    

    # Add a button for each message
    if len(msg) > 0:  
        send_button_clicked = st.button("Send", key=f"send_button_{msg['role']}_{msg['content']}")  # Use message content as a key
        if send_button_clicked:
            # Perform action when the button is clicked
            st.write("Send button clicked!") #send users message to gpt model and display response

    

#streamlit widgets 

#for msg in st.session_state.messages:
    #st.chat_message(msg["role"]).write(msg["content"])
    

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop() 
 #youtube integrating backend        
if st.session_state.messages[-1]["role"] != "assistant": #!= or ==
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = llm_chain.predict(question=prompt)
            st.write(ai_response)
    new_ai_message = {"role": "assistant", "content": ai_response}
    st.session_state.messages.append(new_ai_message)
    chat_history = memory.append("messages") #not supposed to be here 
    
    
    #youtube integrating backend
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)  #pass user prompt into llm model
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    
    #HTTP requests start here. This is not from youtube video. This is from CHATGPT
    
    langchain_endpoint = "http://your-langchain-backend.com/translate"  # Replace with your actual Langchain endpoint
    payload = {"text": prompt}  # Data to send to Langchain for translation
    headers = {"Content-Type": "application/json", "Authorization": "Bearer YOUR_API_KEY"}  # Replace with your actual API key
    response = requests.post(langchain_endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        translated_text = response.json()["translated_text"]
        st.session_state.messages.append({"role": "assistant", "content": translated_text})
        st.chat_message("assistant").write(translated_text)
    else:
        st.error("Failed to translate text. Please try again.")
  

st.write("Message ChatBot...", unsafe_allow_html=True)
#End of HTTP resquests