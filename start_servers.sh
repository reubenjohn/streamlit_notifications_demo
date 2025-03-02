#!/bin/bash

# Clear old log files
rm -f api_log.txt streamlit_log.txt

# Start FastAPI server
echo "Starting FastAPI server..."
python api.py --port 8090 > api_log.txt 2>&1 &
API_PID=$!
echo "FastAPI server started with PID: $API_PID"

# Wait for FastAPI to initialize
sleep 3

# Start Streamlit server
echo "Starting Streamlit server..."
streamlit run app.py > streamlit_log.txt 2>&1 &
STREAMLIT_PID=$!
echo "Streamlit server started with PID: $STREAMLIT_PID"

# Wait for Streamlit to initialize
sleep 5

echo ""
echo "===== Notification Demo Servers Started ====="
echo "FastAPI server:   http://localhost:8090"
echo "Streamlit app:    http://localhost:8501"
echo "Wrapper UI:       http://localhost:8090/streamlit"
echo ""
echo "To test notifications, use the wrapper UI at http://localhost:8090/streamlit"
echo ""
echo "To stop the servers, run: ./stop_servers.sh"
echo "==============================="

# Save PIDs to a file for later use
echo "API_PID=$API_PID" > server_pids.txt
echo "STREAMLIT_PID=$STREAMLIT_PID" >> server_pids.txt