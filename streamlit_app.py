# Import all necessary modules
import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
import database as db


# Store the page icon and title in variables
PAGE_TITLE = "Feedback Form"
PAGE_ICON = "📢"


# Set the page configuration to the title and icon variables defined above
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


# Create a function to load the lottie gif
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        # Use json to load the file
        return json.load(f)

# Load the lottie
feedback_lottie = load_lottie("feedback.json")

# Create a function to load the css file
def local_css(file_name):
    with open(file_name) as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

# Call the function and give the css file as the argument
local_css("styles/main.css")

# Set page header
st.header("🗣️ Feedback Form")

# Create 2 columns
col1, col2 = st.columns(2, gap="small")

# Place the instructions in the first column
with col1: 
    st.subheader("\n**Thank you for using this app!**")
    st.write("-⭐ Rate the app out of 5!")
    st.write("-📢 Send any feedback regarding glitches or issues you may be facing.")

# In the second column, place the lottie
with col2:
    st_lottie(
    feedback_lottie,
)

### RATING WEBSITE

# Function to get user's IP address (so that they dont rate the app twice). Use requests for this.
def get_user_ip():
    try:
        return requests.get('https://api64.ipify.org').text
    except requests.RequestException:
        return None

# Store the IP in user_ip variable
user_ip = get_user_ip()

# Set already rated to True if a user_ip exists, and if it is already present in the Deta database file
already_rated = user_ip is not None and db.has_user_rated(user_ip)

# If already rated is true, then show this message
if already_rated:
    st.write("You have already rated the app. Thank you for your feedback!")

# Otherwise, show the form
else:
    # Create a form
    with st.form("entry_form", clear_on_submit=True):
        
        # Create 3 columns (middle one will be empty so that it is more spaced out)
        a, b, c = st.columns(3, gap="small")

        # Place a slider in the first column
        with a:
            slider_rating = st.slider("**Rate the app!**",1,5)

        # Place the average rating in the third column
        with c:
            # Obtain the average rating through the database.py script
            average_rating = db.get_average_rating()

            # Display the average rating (if it exists)
            if average_rating is not None:
                st.write(f"**Average Rating: {average_rating:.1f} / 5**")

                # Display stars based on the average rating
                stars = "⭐️" * int(average_rating)
                st.write(stars)
            else:
                st.write("No ratings available yet.")

        # Create a button to submit the form
        submitted = st.form_submit_button("Rate!")
        if submitted:
            # Save the user's IP in the database and print a success message
            db.insert_period(slider_rating, user_ip)
            st.success("Thank you for your feedback!")

### ADDITIONAL FEEDBACK FORM

st.write("**Please use the form below for providing any additional feedback or reporting glitches.**")

# Create a contact form using HTML from https://formsubmit.co/ (this is not created by me)
contact_form = f"""
<form action="https://formsubmit.co/e602574ee8e29907086e89985fc692e2" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="https://feedbackform-saaigh.streamlit.app/">
    <input type="text" name="name" placeholder="Your name" required>
    <input type="text" name="organization" placeholder="Your organization (if applicable)">
    <input type="email" name="email" required placeholder="Your email" required>
    <textarea name="message" placeholder="Any feedback/suggestions"></textarea>
    <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)
