import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(page_title="Notification History", page_icon="📜", layout="centered")

# Title
st.title("Notification History")
st.write("View your recent notifications below.")

# Create sample notification data
def generate_sample_notifications(count=10):
    notifications = []
    
    types = ["Message", "Alert", "Update", "Reminder"]
    titles = [
        "New message received", 
        "System update available",
        "Reminder: Upcoming event",
        "Security alert",
        "Battery low",
        "New login detected",
        "Weather alert"
    ]
    
    for i in range(count):
        # Generate a random timestamp within the last 7 days
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        
        notifications.append({
            "timestamp": timestamp,
            "type": random.choice(types),
            "title": random.choice(titles),
            "read": random.choice([True, False]),
        })
    
    # Sort by timestamp (newest first)
    return sorted(notifications, key=lambda x: x["timestamp"], reverse=True)

# Display notifications in a table
notifications = generate_sample_notifications(15)
df = pd.DataFrame(notifications)

# Add formatting
st.dataframe(
    df,
    column_config={
        "timestamp": st.column_config.DatetimeColumn("Time", format="MMM DD, YYYY • hh:mm a"),
        "type": st.column_config.TextColumn("Type"),
        "title": st.column_config.TextColumn("Title"),
        "read": st.column_config.CheckboxColumn("Read"),
    },
    hide_index=True,
)

# Add filter controls
st.divider()
st.subheader("Filter Notifications")

col1, col2 = st.columns(2)
with col1:
    type_filter = st.multiselect("Filter by Type", options=list(set(df["type"])))
with col2:
    read_filter = st.radio("Filter by Status", options=["All", "Read", "Unread"], horizontal=True)

if st.button("Clear All Notifications"):
    st.warning("This would clear all notifications in a real application.")

# Navigation hint
st.divider()
st.info("This is the History page. You can navigate back to the home page via the sidebar.")