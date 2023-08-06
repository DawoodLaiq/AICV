import streamlit as st
from PIL import Image
import fitz  # this is pymupdf

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


st.set_page_config(page_title='AI CV',layout="wide")
st.title('AI CV')
with st.sidebar:
    add_vertical_space(30)
    st.title('SOCIALS:')
    st.markdown('👾 [GITHUB](https://github.com/DawoodLaiq)')
    st.markdown('📰 [LINKEDIN](https://github.com/DawoodLaiq)')


hide_streamlit_style = """
        <style>
        [data-testid="stToolbar"] {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        [data-testid="stSidebarNav"]::before {content: "AI CV";margin-left: 20px;margin-top: 20px;margin-bottom: 20px;font-size: 30px;position: relative;top: 100px;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
container = st.container()
chatcontainer = st.container()
col1, col2 = container.columns(2)
load_dotenv()

def main():
    
    
    col2.header("ABOUT ME")
    #col2.info
    col2.write("I am a Python programmer who likes to solve variety of problems by developing the best solution possible.\n\n"+
    "Any task which can be automated should be automated that's my moto. I have worked with web automation using selenium, web scrapping with Beautiful soup 4, and Desktop app automation with pygui.\n\n"+
    "As a professional I have worked as an EDI Analyst for Ecom specialist LLC. Where I solved multi data related problem and developed clear mapping solution for multi EDI streams.\n\n"+
    "I have a strong interest in machine learning specially in computer vision, I focused on a computer vision based problem in my FYP. Where I detected number plates of vehicles and used OCR to recognize the recognition.\n\n"+
    "I also developed a face verification system for Dubai Leading Technologies which is currently in validation phase."+
    "I am currently expanding my Deep learning knowledge with coursera's DeepLearning.AI specialization.")
    # Display the image
    c1,c2,c3 = col1.columns([1,2,1])
    c2.header("PROFILE")
    img = Image.open('profile.jpeg')
    c2.image(img)
    chatcontainer.header("CHATBOT")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Create a text input for the question at the end
    if prompt :=chatcontainer.chat_input("Enter your question"):
        with chatcontainer.chat_message("assistant"):
            chatcontainer.markdown(prompt)
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
    with chatcontainer.chat_message("user"):
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
