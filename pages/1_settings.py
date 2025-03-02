import streamlit as st

# Set page config
st.set_page_config(page_title="Settings - Firebase Notifications", page_icon="⚙️", layout="centered")

# Title
st.title("Notification Settings")

# Settings form
st.write("Configure your notification preferences below:")

with st.form("notification_settings"):
    st.subheader("General Settings")
    
    enable_notifications = st.toggle("Enable Notifications", value=True)
    notification_sound = st.toggle("Play Sound", value=True)
    
    st.subheader("Notification Types")
    
    notify_direct_messages = st.checkbox("Direct Messages", value=True)
    notify_mentions = st.checkbox("Mentions", value=True)
    notify_updates = st.checkbox("System Updates", value=False)
    
    st.subheader("Time Settings")
    
    quiet_hours = st.toggle("Enable Quiet Hours", value=False)
    
    if quiet_hours:
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input("Start Time", value=None)
        with col2:
            end_time = st.time_input("End Time", value=None)
    
    # Submit button
    submit = st.form_submit_button("Save Settings")
    
    if submit:
        st.success("Settings saved successfully!")
        
# Navigation hint
st.divider()
st.info("This is the Settings page. You can navigate back to the home page via the sidebar.")