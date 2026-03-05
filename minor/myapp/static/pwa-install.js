// PWA Installation Handler
let deferredPrompt;
const installButton = document.getElementById('installButton');

// Check if we're on the home page
function isHomePage() {
  return window.location.pathname === '/' || 
         window.location.pathname === '/home' || 
         window.location.pathname.endsWith('/') ||
         window.location.pathname === '';
}

// Check if app should show install button
function shouldShowInstallButton() {
  // Only show on home page
  if (!isHomePage()) {
    console.log('Not on home page, hiding install button');
    return false;
  }
  
  // Check if app is already installed
  if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    console.log('App is running in standalone mode');
    return false;
  }
  
  return true;
}

// Initialize install button visibility
function initializeInstallButton() {
  if (!installButton) return;
  
  if (shouldShowInstallButton()) {
    console.log('Install button should be available');
    // Don't show immediately, wait for beforeinstallprompt
  } else {
    console.log('Install button should not be shown');
    installButton.style.display = 'none';
  }
}

// Listen for beforeinstallprompt event
window.addEventListener('beforeinstallprompt', (e) => {
  console.log('beforeinstallprompt event fired');
  // Prevent the mini-infobar from appearing on mobile
  e.preventDefault();
  // Stash the event so it can be triggered later
  deferredPrompt = e;
  
  // Show install button only on home page and if conditions are met
  if (shouldShowInstallButton()) {
    console.log('Showing PWA install button on home page');
    if (installButton) {
      installButton.style.display = 'flex';
    }
  }
});

// Install button click handler
if (installButton) {
  installButton.addEventListener('click', async () => {
    if (!deferredPrompt) {
      console.log('No deferred prompt available');
      showNotification('Install not available. Try adding to home screen manually.');
      return;
    }
    // Show the install prompt
    deferredPrompt.prompt();
    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`User response to the install prompt: ${outcome}`);
    // Clear the deferred prompt variable
    deferredPrompt = null;
    // Hide the install button
    if (installButton) installButton.style.display = 'none';
  });
}

// Listen for app installed event
window.addEventListener('appinstalled', () => {
  console.log('PWA was installed');
  if (installButton) installButton.style.display = 'none';
  // Show success message
  showNotification('App installed successfully! You can now use it offline.');
});

// Register Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/service-worker.js')
      .then((registration) => {
        console.log('Service Worker registered successfully:', registration.scope);
        
        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New service worker available
              showUpdateNotification();
            }
          });
        });
      })
      .catch((error) => {
        console.log('Service Worker registration failed:', error);
      });
  });
}

// Show notification helper
function showNotification(message) {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = 'pwa-notification';
  notification.innerHTML = `
    <div class="pwa-notification-content">
      <i class="fas fa-check-circle"></i>
      <span>${message}</span>
    </div>
  `;
  document.body.appendChild(notification);
  
  // Show notification
  setTimeout(() => notification.classList.add('show'), 100);
  
  // Hide after 3 seconds
  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Show update notification
function showUpdateNotification() {
  const updateBanner = document.createElement('div');
  updateBanner.className = 'update-banner';
  updateBanner.innerHTML = `
    <div class="update-banner-content">
      <span>New version available!</span>
      <button onclick="window.location.reload()" class="update-btn">Update</button>
    </div>
  `;
  document.body.appendChild(updateBanner);
}

// Handle online/offline status
window.addEventListener('online', () => {
  showNotification('You are back online!');
});

window.addEventListener('offline', () => {
  showNotification('You are offline. Some features may be limited.');
});

// Add to home screen prompt for iOS
function isIOS() {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
}

function isInStandaloneMode() {
  return ('standalone' in window.navigator) && (window.navigator.standalone);
}

if (isIOS() && !isInStandaloneMode()) {
  // Show iOS install instructions
  const iosPrompt = document.getElementById('iosInstallPrompt');
  if (iosPrompt) {
    iosPrompt.style.display = 'block';
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeInstallButton();
});
