chrome.runtime.onInstalled.addListener(() => {
    console.log("ScamSaver Extension Installed");
  });
  
  // Function to save email content and attachments to storage
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'saveEmail') {
      const emailData = {
        emailText: request.emailText,
        attachments: request.attachments,
        timestamp: new Date().toISOString(),
      };
      chrome.storage.local.set({ emailData: emailData }, () => {
        sendResponse({ status: 'success' });
      });
      return true;  // Keep the message channel open for async response
    }
  });
  