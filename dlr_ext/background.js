// DLR Session Keeper - Service Worker
// Monitors messages from content script and stores/restores tokens

// On install, nothing special needed
chrome.runtime.onInstalled.addListener(() => {
  console.log('DLR Session Keeper installed');
});

// Listen for token updates from content script
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'token_update' && msg.token) {
    chrome.storage.local.set({ discord_token: msg.token }, () => {
      sendResponse({ status: 'saved' });
    });
    return true; // Keep channel open for async response
  }
  if (msg.type === 'get_token') {
    chrome.storage.local.get('discord_token', (data) => {
      sendResponse({ token: data.discord_token || null });
    });
    return true;
  }
  if (msg.type === 'token_cleared') {
    chrome.storage.local.remove('discord_token', () => {
      sendResponse({ status: 'cleared' });
    });
    return true;
  }
  if (msg.type === 'check_alive') {
    sendResponse({ alive: true });
  }
});

// Auto-clear expired tokens (check every hour)
setInterval(() => {
  chrome.storage.local.get('discord_token', (data) => {
    if (data.discord_token && data.discord_token.length < 20) {
      chrome.storage.local.remove('discord_token');
    }
  });
}, 3600000);
