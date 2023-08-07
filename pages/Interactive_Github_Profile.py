import streamlit as st
from PIL import Image
from streamlit_extras.add_vertical_space import add_vertical_space
import io
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import altair as alt

st.set_page_config(page_title='AI CV',layout="wide")

with st.sidebar:
    add_vertical_space(30)
    st.title('SOCIALS:')
    st.markdown('👾 [GITHUB](https://github.com/DawoodLaiq)')
    st.markdown('📰 [LINKEDIN](https://github.com/DawoodLaiq)')

st.header("GITHUB PROJECTS READMEs")
hide_streamlit_style = """
        <style>
        [data-testid="stToolbar"] {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        [data-testid="stSidebarNav"]::before {content: "AI CV";margin-left: 20px;margin-top: 20px;margin-bottom: 20px;font-size: 30px;position: relative;top: 100px;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def get_github_data():
        # Your GitHub token
    TOKEN = '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'
    # Headers
    headers = {
        'Authorization': f'bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    data_query = """
    {
    user(login: "USERNAME") {
        repositories(first: 100) {
        nodes {
            name
            url
            description
            readme: object(expression: "main:README.md") {
            ... on Blob {
                text
            }
            }
        }
        }
    }
    }
    """
    # Replace USERNAME placeholder with the desired GitHub username
    data_query = data_query.replace('USERNAME', 'DawoodLaiq')

    response = requests.post('https://api.github.com/graphql', json={'query': data_query}, headers=headers)
    json_data = response.json()

    return json_data



json_data = get_github_data()
repos = json_data["data"]["user"]["repositories"]["nodes"]
with st.expander("See all readme of the projects"):
    for repo in repos:
        # Check if readme key exists and is not null
        
        if repo["readme"] and repo["readme"]["text"]:
            #st.header(f"Repository Name: {repo['name']}")
            st.markdown(repo['readme']['text'])
            st.divider()
            st.divider()