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
    
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/static/img/firebase-logo.svg'
    };
    
    self.registration.showNotification(notificationTitle, notificationOptions);
});