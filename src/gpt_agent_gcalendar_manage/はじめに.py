import streamlit as st
from views.common import init_screen
from services.chat_bot import init_gpt

st.set_page_config(layout='wide')
init_screen()
with open('./assets/introduction.md', 'r') as f:
    readme = f.read()
st.markdown(readme)