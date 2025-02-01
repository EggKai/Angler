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
});
  