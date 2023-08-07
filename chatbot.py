import os
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import time
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self, chat_container, st_module):
        self.chatcontainer = chat_container
        self.st = st_module

    def handle_question_submit(self, question):
        data, store_name = self.get_pdf_data()

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
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)

        docs = VectorStore.similarity_search(query=question, k=3)
        llm = OpenAI()
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=question)
            print(cb)
        
        self.display_response(response)

    def get_pdf_data(self):
        with open("Sanjin Dedic Resume.pdf", "rb") as f:
            store_name = f.name[:-4]
            pdf_reader = PdfReader(f)
            data = ""
            for page in pdf_reader.pages:
                data += page.extract_text()

        return data, store_name

    def display_response(self, response):
        answer = f"{response}"
        with self.chatcontainer.chat_message("user"):
            message_placeholder = self.st.empty()
            full_response = ""
            for chunk in answer.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Append the message to the session state
        self.st.session_state.messages.append({"role": "user", "content": answer})