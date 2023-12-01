import streamlit as st
from pathlib import Path
from streamlit_lottie import st_lottie
import json

import database as db


# Store the page icon and title in variables
PAGE_TITLE = "Feedback Form"
PAGE_ICON = "📢"


# Set the page configuration to the title and icon variables defined above
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

@st.cache_data
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        # Use json to load the file
        return json.load(f)

def local_css(file_name):
    with open(file_name) as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

local_css("styles/main.css")

st.header("🗣️ Feedback Form")

col1, col2 = st.columns(2, gap="small")

# Place the instructions in the first column
with col1: 
    st.subheader("\n**Thank you for using this app!**")
    st.write("-⭐ Rate the app out of 5!")
    st.write("-📢 Send any feedback regarding glitches or issues you may be facing.")

feedback_lottie = load_lottie("feedback.json")

with col2:
    st_lottie(
    feedback_lottie,
)
    
with st.form("entry_form", clear_on_submit=True):

    a, b, c, d = st.columns(4, gap="small")

    with a:
        slider_rating = st.slider("**Rate the app!**",1,5)

    submitted = st.form_submit_button("Rate!")
    if submitted:
        db.insert_period(slider_rating)
        st.success("Thank you for your feedback!")

st.write("**Please use the form below for providing any additional feedback or reporting glitches.**")

contact_form = f"""
<form action="https://formsubmit.co/saaight519@deltalearns.ca" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="text" name="name" placeholder="Your name" required>
    <input type="text" name="organization" placeholder="Your organization (if applicable)">
    <input type="email" name="email" required placeholder="Your email" required>
    <textarea name="message" placeholder="Any feedback/suggestions"></textarea>
    <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)
