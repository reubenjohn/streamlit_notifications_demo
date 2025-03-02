# Streamlit Notifications Demo

A demonstration of Firebase Cloud Messaging (FCM) push notifications with a Streamlit frontend and FastAPI backend. This project shows how to overcome Streamlit's iframe constraints to enable web push notifications.

## Architecture

This demo uses a wrapper-based approach to enable web push notifications in Streamlit:

1. **FastAPI Backend**: Handles Firebase initialization, manages subscriptions, and sends notifications
2. **HTML Wrapper**: Serves as the parent page that:
   - Registers the Firebase service worker (required for notifications)
   - Embeds the Streamlit app in an iframe
   - Provides notification controls in a header above the Streamlit UI
3. **Firebase Cloud Messaging**: Delivers push notifications to the browser

## Requirements

- Python 3.10+
- Poetry for dependency management
- Firebase project with Cloud Messaging enabled
- Firebase service account credentials

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install poetry
   poetry install
   ```
3. Create a `.env` file in the project root with your Firebase configuration:
   ```
   # Firebase Service Account for Admin SDK
   SERVICE_ACCOUNT_KEY_PATH=/path/to/your-firebase-service-account.json

   # Firebase Web Configuration
   FIREBASE_API_KEY=your-api-key
   FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
   FIREBASE_APP_ID=your-app-id
   FIREBASE_MEASUREMENT_ID=your-measurement-id
   FIREBASE_VAPID_KEY=your-vapid-key
   
   # Streamlit Configuration
   STREAMLIT_URL=http://localhost:8501
   ```
   
   You can copy the `.env.example` file as a starting point.

## Running the Demo

### Using the convenience scripts (recommended)

1. Start both servers with a single command:
   ```bash
   ./start_servers.sh
   ```

2. Access the demo:
   - Plain Streamlit app (no notifications): http://localhost:8501
   - **Streamlit with notifications**: http://localhost:8090/streamlit ← Use this for testing

3. Stop the servers when done:
   ```bash
   ./stop_servers.sh
   ```

### Running servers manually (alternative)

1. Start the FastAPI backend:
   ```bash
   python api.py --port 8090
   ```

2. In another terminal, start Streamlit:
   ```bash
   streamlit run app.py
   ```

## How It Works

1. **Service Worker Registration**: The wrapper HTML page registers the Firebase service worker at the root scope
2. **Notification Permission**: When the user enables notifications, the browser requests permission
3. **Token Registration**: The browser receives an FCM token and sends it to the FastAPI backend
4. **Notification Delivery**: 
   - When "Test Notification" is clicked, a request is sent to the backend
   - The backend sends individual messages to each registered token using Firebase Admin SDK
   - Firebase delivers the notifications to the browsers

## Technical Details

- The service worker must be served from the root path (`/firebase-messaging-sw.js`)
- Notifications use individual Firebase Admin SDK messages rather than batch/multicast messages
- The Streamlit UI is embedded in the wrapper page via an iframe
- Token registration persists only for the current server session (not stored permanently)

## Deployment

For production deployment, you can use:

1. A reverse proxy like Nginx to serve both services on a single domain
2. Environment variables to configure Firebase credentials:
   - Set all `FIREBASE_*` variables directly in your hosting environment 
   - Or use a `.env` file as described in the setup section
3. A database to persistently store FCM tokens