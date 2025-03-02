# Streamlit with Firebase Push Notifications (Multi-page Navigation Demo)

This project demonstrates a working implementation of Firebase Cloud Messaging (FCM) push notifications with a Streamlit application, with a focus on supporting correct navigation to Streamlit sub-pages.

## Current Goal

Having successfully implemented and demonstrated Firebase push notifications with Streamlit, our current goal is to:

1. Implement sub-pages in the Streamlit application
2. Ensure users can navigate to specific Streamlit sub-pages via the FastAPI wrapper
3. Modify the wrapper to correctly handle sub-page navigation through the iframe
4. Validate that all functionality works seamlessly including the push notifications

## Development Guidelines

- Make git commits often as you make progress, but don't push them
- When launching servers, use background processes for testing (see start_servers.sh)
- Use curl or browser testing to validate functionality
- Restart servers when changing backend code for changes to take effect
- Don't install new dependencies without asking first
- For browser validation, launch the servers give the human instructions to follow
- All testing results will be recorded in human_testing_results.txt

## How to Use This Repository

- Start both servers with: `./start_servers.sh`
- Configure and start Nginx with: `sudo ./config_nginx.sh <port>`  
- Access the application at: http://localhost:<port>/
- Stop servers with: `./stop_servers.sh`

## Major Findings

1. **Streamlit Service Worker Limitation**: As suspected, Streamlit's architecture (using iframes) prevents direct Firebase Cloud Messaging service worker registration, resulting in the error: "We are unable to register the default service worker. Failed to register a ServiceWorker: The document is in an invalid state."

2. **Solution Implemented**: Created a wrapper HTML page served by FastAPI that:
   - Handles Firebase service worker registration at the root scope
   - Embeds the Streamlit app in an iframe
   - Provides notification buttons in a header above the Streamlit UI

   **Key Files Created/Modified:**
    - app.py: Simple Streamlit app
    - api.py: FastAPI backend with Firebase integration
    - static/streamlit_wrapper.html: Wrapper page hosting Streamlit + notifications
    - static/firebase-messaging-sw.js: Service worker for FCM
    - start_servers.sh/stop_servers.sh: Convenience scripts

3. **Service Worker Path**: The service worker must be served from the root path (`/firebase-messaging-sw.js`) with the correct Content-Type (`application/javascript`). We added a dedicated endpoint in FastAPI to serve this file correctly.

4. **Firebase Initialization**: Fixed two key issues:
   - First, we handled the case where Firebase was being initialized twice when using auto-reload in development mode
   - Second, we fixed the module loading approach to properly check for existing Firebase app instances

5. **Firebase Cloud Messaging API Issues**: Discovered that the Firebase Admin SDK's `messaging.send_multicast()` method was unreliable:
   - It consistently resulted in 404 errors to Google's `/batch` endpoint
   - Resolved by using individual message sending via `messaging.send()` instead
   - Each notification token is processed individually rather than in batch

6. **Error Handling**: Implemented improved error handling throughout the application, with clear status messages in the UI and detailed logging

7. **Nginx Configuration Insights**:
   - Service worker must be served from the same origin as the main page
   - Proxy configuration must properly handle WebSocket connections for Streamlit
   - Specific API endpoints need separate location blocks for proper routing
   - Static files should be served with appropriate cache headers

