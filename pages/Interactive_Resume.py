import streamlit as st
from PIL import Image
import fitz
from streamlit_extras.add_vertical_space import add_vertical_space
st.set_page_config(page_title='AI CV',layout="wide")

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

st.header("Interactive Resume")
container = st.container()
col1,col2 = container.columns(2)
c1,c2,c3 = col1.columns(3)
cd1,cd2,cd3 = col2.columns([1,1,1])
with fitz.open("Sanjin Dedic Resume.pdf") as doc:
    max_pages = len(doc)
    session_state = st.session_state
    if "page" not in session_state:
        session_state.page = 1
    if c1.button('Previous', use_container_width=True) and session_state.page > 1:
        session_state.page -= 1
    if c3.button('Next', use_container_width=True) and session_state.page < max_pages:
        session_state.page += 1

    page = doc.load_page(session_state.page - 1)  # zero-based index
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = img.resize((img.size[0], 800))
    # Display the image
    col1.image(img, caption=f"Page {session_state.page}")

with cd2:
    add_vertical_space(15)

with open("Sanjin Dedic Resume.pdf", "rb") as f:
    cd2.download_button('Download 3 page resume', f,f.name+".pdf")

with open("Sanjin Dedic Resume.pdf", "rb") as f:
    cd2.download_button('Download 10 page resume', f,f.name+".pdf")