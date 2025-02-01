chrome.runtime.onInstalled.addListener(() => {
    console.log("Angler Extension Installed");
  });
  
// Function to save email content and attachments to storage
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'saveEmail') {
    const { Spam, Phishing, LLM, urls, Code, Executables } = request.emailData;
    const emailData = {
      Spam: Spam,
      Phishing : Phishing,
      LLM : LLM,
      urls : urls,
      Code: Code,
      Executables: Executables,
      timestamp: new Date().toISOString(),
    };
    chrome.storage.local.set({emailData: emailData} , () => {
      sendResponse({ status: 'success' });
    });
    return true;  // Keep the message channel open for async respons  e
  }
  if (request.action === 'clearEmail') {
    chrome.storage.local.remove('emailData', () => {
      sendResponse({ status: 'cleared' });
    });
    chrome.storage.local.remove('busy', () => {
      sendResponse({ status: 'free' });
    });
    return true;  // Keep the message channel open for async response
  }
  if (request.action === 'busy') {
    chrome.storage.local.set({busy: true} , () => {
      sendResponse({ status: 'busy' });
    });
    return true;  // Keep the message channel open for async response
  }
});
  