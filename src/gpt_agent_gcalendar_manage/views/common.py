from pathlib import Path

import pandas as pd
import streamlit as st

def init_screen():
    st.markdown("""
            <style>
                .block-container {
                        padding-top: 1rem;
                        padding-bottom: 0rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
            </style>
            """, unsafe_allow_html=True)
    # セッション情報
    if 'conversation_list' not in st.session_state:
        st.session_state['conversation_list'] = []