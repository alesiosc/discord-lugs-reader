// DLR Session Keeper - Content Script
// Runs on every Discord page load. Saves token when it appears, restores if missing.

(function() {
  'use strict';

  const SAVE_INTERVAL = 5000; // Check every 5 seconds
  let lastToken = null;
  let restoreAttempted = false;

  function getToken() {
    try {
      return localStorage.getItem('token');
    } catch(e) {
      return null;
    }
  }

  function setToken(token) {
    try {
      localStorage.setItem('token', token);
      return true;
    } catch(e) {
      return false;
    }
  }

  function notifyBackground(msg) {
    try {
      chrome.runtime.sendMessage(msg);
    } catch(e) {
      // Extension context may not be ready yet
    }
  }

  // Try to restore token on page load
  function attemptRestore() {
    if (restoreAttempted) return;
    restoreAttempted = true;

    const currentToken = getToken();
    if (currentToken && currentToken.length > 20) {
      // Already have a valid token, save it to storage
      lastToken = currentToken;
      notifyBackground({ type: 'token_update', token: currentToken });
      console.log('DLR: Existing valid discord token');
      return;
    }

    // Token missing or invalid, try to restore from storage
    chrome.runtime.sendMessage({ type: 'get_token' }, (response) => {
      if (response && response.token && response.token.length > 20) {
        setToken(response.token);
        lastToken = response.token;
        console.log('DLR: Restored discord token from storage');
        // Reload to apply restored token
        location.reload();
      } else {
        console.log('DLR: No saved token to restore, needs manual login');
      }
    });
  }

  // Monitor token changes
  function monitorToken() {
    const token = getToken();
    if (!token || token.length < 5) {
      return; // No token present yet
    }

    if (token !== lastToken) {
      lastToken = token;
      if (token.length > 20) {
        notifyBackground({ type: 'token_update', token });
        console.log('DLR: Saved updated discord token');
      }
    }
  }

  // Run restore first
  attemptRestore();

  // Then monitor for changes
  setInterval(monitorToken, SAVE_INTERVAL);

  // Also watch for localStorage changes via storage event
  window.addEventListener('storage', (e) => {
    if (e.key === 'token' && e.newValue && e.newValue.length > 20) {
      lastToken = e.newValue;
      notifyBackground({ type: 'token_update', token: e.newValue });
    }
  });
})();
