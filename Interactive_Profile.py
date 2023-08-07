import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from chatbot import Chatbot


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
    chatbot = Chatbot(chatcontainer, st)

    # Create a text input for the question at the end
    if prompt := chatcontainer.chat_input("Enter your question"):
        with chatcontainer.chat_message("assistant"):
            chatcontainer.markdown(prompt)
        st.session_state.messages.append({"role": "assistant", "content": prompt})
        chatbot.handle_question_submit(prompt)


if __name__=="__main__":
    main()
