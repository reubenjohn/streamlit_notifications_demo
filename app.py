import streamlit as st
import requests
import json

# Set page config
st.set_page_config(page_title="Firebase Notifications Demo", page_icon="🔔", layout="centered")

# Title
st.title("Firebase Notifications Demo")
st.write(
    "This is a simple Streamlit app that demonstrates Firebase notifications with multiple pages."
)

# Information section
st.divider()
st.subheader("How Notifications Work")
st.write(
    """
This demo uses Firebase Cloud Messaging (FCM) to enable browser notifications.

When used within the wrapper UI (http://localhost:8090), you can:
1. Enable notifications with the button in the top header
2. Send test notifications using the button in the top header

The wrapper UI is necessary because Streamlit's iframe architecture prevents direct 
service worker registration, which is required for Firebase notifications.
"""
)

# Navigation section
st.divider()
st.subheader("Navigation")
st.write(
    """
This demo includes multiple pages to demonstrate navigation:
1. Home (this page)
2. Settings - configuring notification preferences
3. History - viewing past notifications

Use the sidebar to navigate between pages, or try accessing pages directly via URL:
- http://localhost:8090/settings
- http://localhost:8090/history
"""
)

# Status section
st.divider()
st.subheader("Backend Status")

if st.button("Check Backend Status"):
    try:
        # Try to send a test request to the backend
        response = requests.get("http://localhost:8090/")
        if response.status_code == 200:
            st.success("Backend is running and accessible!")
        else:
            st.error(f"Backend returned error code: {response.status_code}")
    except Exception as e:
        st.error(f"Could not connect to backend: {str(e)}")
        st.info("Make sure the FastAPI backend is running on port 8090")
