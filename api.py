from contextlib import asynccontextmanager
import os
import logging
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from typing import Dict, Any
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("api")

# Load environment variables from .env file at startup
load_dotenv(".env", override=True, verbose=True)

from naomi_core.db import WebhookEvent, initialize_db, session_scope
from firebase_admin import initialize_app, credentials, messaging  # type: ignore[import]

# Load Firebase configuration from environment variables
firebase_config = {
    "apiKey": os.environ.get("FIREBASE_API_KEY", ""),
    "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN", ""),
    "projectId": os.environ.get("FIREBASE_PROJECT_ID", ""),
    "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", ""),
    "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID", ""),
    "appId": os.environ.get("FIREBASE_APP_ID", ""),
    "measurementId": os.environ.get("FIREBASE_MEASUREMENT_ID", ""),
    "vapidKey": os.environ.get("FIREBASE_VAPID_KEY", ""),
}

# Log if Firebase configuration was loaded
if firebase_config["apiKey"]:
    logger.info("Loaded Firebase configuration from environment variables")
else:
    logger.warning("Firebase configuration not found in environment variables")

# Initialize Firebase with credentials
firebase_initialized = False
try:
    # Get service account path (with fallback to default)
    service_account_path = os.environ.get("SERVICE_ACCOUNT_KEY_PATH")

    # Validate the service account path exists
    if not os.path.exists(service_account_path):
        logger.error(f"Firebase service account file not found at: {service_account_path}")
    else:
        logger.info(f"Using Firebase service account from: {service_account_path}")

        # Check if Firebase app is already initialized
        try:
            from firebase_admin import _apps

            if _apps:
                firebase_initialized = True
                logger.info(f"Firebase already initialized, using existing app")
            else:
                # Initialize Firebase with the service account
                cred = credentials.Certificate(service_account_path)
                initialize_app(cred)
                firebase_initialized = True
                logger.info(f"Firebase initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}", exc_info=True)
except Exception as e:
    logger.error(f"Failed to initialize Firebase: {e}", exc_info=True)

# Store FCM tokens from subscribers
subscribers = []


# Application lifecycle manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    try:
        initialize_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize database: {e}")
    yield


# Create FastAPI application
app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow browser connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Get Streamlit URL from environment variables
STREAMLIT_URL = os.environ.get("STREAMLIT_URL")
logger.info(f"Using Streamlit URL: {STREAMLIT_URL}")


# Helper function to inject configuration into HTML templates
def inject_firebase_config(html_content):
    if not firebase_config:
        return html_content

    # Simple placeholder replacements
    replacements = {
        "PLACEHOLDER_FIREBASE_API_KEY": firebase_config.get("apiKey", ""),
        "PLACEHOLDER_FIREBASE_AUTH_DOMAIN": firebase_config.get("authDomain", ""),
        "PLACEHOLDER_FIREBASE_PROJECT_ID": firebase_config.get("projectId", ""),
        "PLACEHOLDER_FIREBASE_STORAGE_BUCKET": firebase_config.get("storageBucket", ""),
        "PLACEHOLDER_FIREBASE_MESSAGING_SENDER_ID": firebase_config.get("messagingSenderId", ""),
        "PLACEHOLDER_FIREBASE_APP_ID": firebase_config.get("appId", ""),
        "PLACEHOLDER_FIREBASE_MEASUREMENT_ID": firebase_config.get("measurementId", ""),
        "PLACEHOLDER_VAPID_KEY": firebase_config.get("vapidKey", ""),
        "PLACEHOLDER_STREAMLIT_URL": STREAMLIT_URL,
    }

    # Perform all replacements
    for placeholder, value in replacements.items():
        html_content = html_content.replace(placeholder, value)

    return html_content


# Root endpoint - serve test.html
@app.get("/html_test", response_class=HTMLResponse)
async def get_html():
    with open("static/test.html") as f:
        content = f.read()
    return inject_firebase_config(content)


# Streamlit wrapper endpoint
@app.get("/", response_class=HTMLResponse)
async def get_streamlit_wrapper():
    with open("static/streamlit_wrapper.html") as f:
        content = f.read()
    return inject_firebase_config(content)


# Firebase service worker endpoint (must be served from root path)
@app.get("/firebase-messaging-sw.js")
async def get_service_worker():
    with open("static/firebase-messaging-sw.js") as f:
        content = f.read()

    # Use the same inject_firebase_config helper for consistency
    content = inject_firebase_config(content)

    return Response(content=content, media_type="application/javascript")


# Data model for webhook events
class WebhookEventRequest(BaseModel):
    type: str
    payload: Dict[str, Any]


# Webhook endpoint
@app.post("/webhook")
async def receive_webhook(event: WebhookEventRequest):
    with session_scope() as session:
        new_event = WebhookEvent(event_type=event.type, payload=str(event.payload))
        session.add(new_event)
    return {"status": "OK"}


# Subscribe endpoint - register FCM tokens
@app.post("/subscribe")
async def subscribe(data: dict):
    token = data.get("token")
    if token not in subscribers:
        subscribers.append(token)
        logger.info(f"New FCM token registered, total subscribers: {len(subscribers)}")
    return {"message": "Subscribed", "token": token}


# Send notification endpoint - using individual messages with the Firebase Admin SDK
@app.post("/send_notification")
async def send_notification():
    """Send notifications to all subscribers using Firebase Admin SDK's individual message API"""
    if not firebase_initialized:
        logger.error("Firebase not initialized. Cannot send notifications.")
        return {
            "error": "Firebase not initialized",
            "success_count": 0,
        }

    if not subscribers:
        logger.warning("No subscribers to send notifications to.")
        return {
            "message": "No subscribers to send notifications to. Enable notifications first.",
            "success_count": 0,
        }

    try:
        logger.info(f"Sending notification to {len(subscribers)} subscribers")

        # Track successful sends
        success_count = 0
        failure_count = 0

        # Send to each token individually (multicast messages don't work reliably)
        for idx, token in enumerate(subscribers):
            try:
                # Create message for this token
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Test Notification",
                        body="This is a test notification from Firebase Cloud Messaging",
                    ),
                    data={"score": "850", "time": "2:45"},
                    token=token,
                )

                # Send the message
                message_id = messaging.send(message)

                # Track result
                success_count += 1
                logger.info(f"Successfully sent notification {message_id=} to token {idx+1}")

            except Exception as token_error:
                failure_count += 1
                logger.error(f"Error sending to token {idx+1}: {token_error}")

        # Return results summary
        return {
            "message": f"Sent {success_count} notifications successfully, {failure_count} failed",
            "success_count": success_count,
            "failure_count": failure_count,
        }

    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return {"error": str(e), "success_count": 0}


def main():
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="Run the FastAPI server.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8090, help="Port to run the server on")
    args = parser.parse_args()

    logger.info(f"Starting server at http://{args.host}:{args.port}")
    logger.info("- For Firebase demo, visit: http://localhost:8090/")
    logger.info("- For Streamlit with notifications: http://localhost:8090/streamlit")

    uvicorn.run("api:app", host=args.host, port=args.port, reload=True)


if __name__ == "__main__":
    main()
