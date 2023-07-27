import streamlit as st
import pickle
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
import time

st.set_page_config(page_title='AI CV')
st.title('AI CV')

with st.sidebar:
    st.title('TEST')
    st.markdown('''
            ###AI CV
            This is the app testing''')
    add_vertical_space(5)
    st.write('Testing phase')

hide_streamlit_style = """
        <style>
        [data-testid="stToolbar"] {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

load_dotenv()

def main():
    
    st.header("main window")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Create a text input for the question at the end
    if prompt :=st.chat_input("Enter your question"):
        with st.chat_message("assistant"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "assistant", "content": prompt})
        handle_question_submit(prompt)

def handle_question_submit(question):
    
    data,store_name=get_pdf_data()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text=data)
    

    if os.path.exists(f"{store_name}.pkl"):
        with open(f"{store_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
    else:
        embeddings = OpenAIEmbeddings()
        VectorStore = FAISS.from_texts(chunks,embedding=embeddings)
        
        with open(f"{store_name}.pkl", "wb") as f:
            pickle.dump(VectorStore, f)

    docs = VectorStore.similarity_search(query=question, k=3)
    llm = OpenAI()
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=question)
        print(cb)
    
    
    
    answer = f"{response}"
    with st.chat_message("user"):
        st.write("Hello User 👋")
        message_placeholder = st.empty()
        full_response=""
        for chunk in answer.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "user", "content": answer})

    
        

        
def get_pdf_data():
    with open("Sanjin Dedic Resume.pdf", "rb") as f:
        store_name = f.name[:-4]
        pdf_reader = PdfReader(f)
        data=""
        for page in pdf_reader.pages:
            data += page.extract_text()

    return data,store_name

if __name__=="__main__":
    main()
