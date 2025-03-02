// Firebase messaging service worker
importScripts('https://www.gstatic.com/firebasejs/11.3.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/11.3.1/firebase-messaging-compat.js');

const firebaseConfig = {
    apiKey: "PLACEHOLDER_FIREBASE_API_KEY",
    authDomain: "PLACEHOLDER_FIREBASE_AUTH_DOMAIN",
    projectId: "PLACEHOLDER_FIREBASE_PROJECT_ID",
    storageBucket: "PLACEHOLDER_FIREBASE_STORAGE_BUCKET",
    messagingSenderId: "PLACEHOLDER_FIREBASE_MESSAGING_SENDER_ID",
    appId: "PLACEHOLDER_FIREBASE_APP_ID",
    measurementId: "PLACEHOLDER_FIREBASE_MEASUREMENT_ID"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

// Background message handling
messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);

    const notificationTitle = `${payload.notification.title} [Background]`;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/static/img/firebase-logo.svg',
        // Add data with URL to open when clicked
        data: {
            url: payload.data?.click_action || payload.data?.url || 'http://localhost:8090'
        }
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});

// Add click handler for the notifications
self.addEventListener('notificationclick', function (event) {
    console.log('[firebase-messaging-sw.js] Notification click detected', event);

    event.notification.close();

    // Get the URL from notification data, fallback to root URL
    const urlToOpen = event.notification.data.url || 'http://localhost:8090';

    // This will use the URL specified in the notification payload
    event.waitUntil(
        clients.matchAll({ type: 'window' }).then(windowClients => {
            // Check if there is already a window/tab open with the target URL
            for (var i = 0; i < windowClients.length; i++) {
                var client = windowClients[i];
                // If so, just focus it.
                if (client.url === urlToOpen && 'focus' in client) {
                    return client.focus();
                }
            }
            // If not, open a new window.
            if (clients.openWindow) {
                return clients.openWindow(urlToOpen);
            }
        })
    );
});