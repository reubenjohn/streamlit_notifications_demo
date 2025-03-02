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
   # Firebase Web Configuration
   FIREBASE_API_KEY=your-api-key
   FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
   FIREBASE_APP_ID=your-app-id
   FIREBASE_MEASUREMENT_ID=your-measurement-id
   FIREBASE_VAPID_KEY=your-vapid-key
   
   # Firebase Admin SDK Configuration (from service account JSON)
   FIREBASE_ADMIN_TYPE=service_account
   FIREBASE_ADMIN_PRIVATE_KEY_ID=your-private-key-id
   FIREBASE_ADMIN_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nyour-private-key-content-with-newlines\n-----END PRIVATE KEY-----\n
   FIREBASE_ADMIN_CLIENT_EMAIL=your-project@your-project-id.iam.gserviceaccount.com
   FIREBASE_ADMIN_CLIENT_ID=your-client-id
   FIREBASE_ADMIN_AUTH_URI=https://accounts.google.com/o/oauth2/auth
   FIREBASE_ADMIN_TOKEN_URI=https://oauth2.googleapis.com/token
   FIREBASE_ADMIN_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
   FIREBASE_ADMIN_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-project%40your-project-id.iam.gserviceaccount.com
   FIREBASE_ADMIN_UNIVERSE_DOMAIN=googleapis.com
   
   # Streamlit Configuration
   STREAMLIT_URL=http://localhost:8501
   ```
   
   You can copy the `.env.example` file as a starting point. Note that for the `FIREBASE_ADMIN_PRIVATE_KEY`, you need to include the actual private key with newlines represented as `\n`.

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

### Railway Deployment

This project includes a `railway.toml` configuration for easy deployment on [Railway](https://railway.app/):

1. The configuration deploys only the FastAPI backend (not Streamlit)
2. Configure the following environment variables in your Railway project:
   - All the Firebase Web Configuration variables:
     - `FIREBASE_API_KEY`: Your Firebase Web API Key
     - `FIREBASE_AUTH_DOMAIN`: Your Firebase auth domain
     - `FIREBASE_PROJECT_ID`: Your Firebase project ID
     - `FIREBASE_STORAGE_BUCKET`: Your Firebase storage bucket
     - `FIREBASE_MESSAGING_SENDER_ID`: Your Firebase messaging sender ID
     - `FIREBASE_APP_ID`: Your Firebase app ID
     - `FIREBASE_MEASUREMENT_ID`: Your Firebase measurement ID
     - `FIREBASE_VAPID_KEY`: Your Firebase VAPID key
   - All the Firebase Admin SDK Configuration variables:
     - `FIREBASE_ADMIN_TYPE`: Usually "service_account"
     - `FIREBASE_ADMIN_PRIVATE_KEY_ID`: Your Firebase private key ID
     - `FIREBASE_ADMIN_PRIVATE_KEY`: Your Firebase private key (with newlines as \n)
     - `FIREBASE_ADMIN_CLIENT_EMAIL`: Your Firebase client email
     - `FIREBASE_ADMIN_CLIENT_ID`: Your Firebase client ID
     - `FIREBASE_ADMIN_AUTH_URI`: Authentication URI
     - `FIREBASE_ADMIN_TOKEN_URI`: Token URI
     - `FIREBASE_ADMIN_AUTH_PROVIDER_CERT_URL`: Auth provider cert URL
     - `FIREBASE_ADMIN_CLIENT_CERT_URL`: Client cert URL
     - `FIREBASE_ADMIN_UNIVERSE_DOMAIN`: Usually "googleapis.com"
   - `STREAMLIT_URL`: URL to your separately deployed Streamlit app

3. Deploy your Streamlit app separately (on Railway or another platform)
4. Point `STREAMLIT_URL` to your deployed Streamlit URL

### Other Deployment Options

For other deployment scenarios:

1. Environment variables to configure Firebase credentials:
   - Set all `FIREBASE_*` variables directly in your hosting environment 
   - Or use a `.env` file as described in the setup section
2. Consider using a database to persistently store FCM tokens