#!/bin/bash

# Load PIDs from the file if it exists
if [ -f server_pids.txt ]; then
    source server_pids.txt
    
    # Check if we have valid PIDs
    if [ -n "$API_PID" ] && [ -n "$STREAMLIT_PID" ]; then
        echo "Stopping FastAPI server (PID: $API_PID)..."
        kill $API_PID 2>/dev/null || echo "FastAPI server was not running"
        
        echo "Stopping Streamlit server (PID: $STREAMLIT_PID)..."
        kill $STREAMLIT_PID 2>/dev/null || echo "Streamlit server was not running"
        
        echo "All servers stopped."
        rm server_pids.txt
    else
        echo "No valid PIDs found in server_pids.txt"
    fi
else
    echo "No server_pids.txt file found. Servers may not be running."
    echo "Try: ps aux | grep 'python api.py\\|streamlit run' to find PIDs"
fi