// Variable to store the last processed email's identifier
let lastProcessedEmailId = '';

// Define the API endpoint and the token
const apiUrl = 'http://localhost:5000/send_data';  // Update this to your Flask server's URL
const apiToken = 'token';  // The same token you define in your Flask server

// Function to extract email text
function extractEmailText() {
  const emailBody = document.querySelector('.a3s.aiL');
  return emailBody ? emailBody.textContent : '';
}

// Function to extract URLs from the email body
function extractUrls() {
  const emailBody = document.querySelector('.a3s.aiL');
  const imageLinks = [];
  if (emailBody) {
    const urlElements = emailBody.querySelectorAll('a');
    urlElements.forEach((url) => {
      if (url.href) {
        imageLinks.push(url.href);  // Extract the URL
      }
    });
  }
  return imageLinks;
}

// Function to extract image links from the email body
function extractImageLinks() {
  const emailBody = document.querySelector('.a3s.aiL');
  const imageLinks = [];
  if (emailBody) {
    const imageElements = emailBody.querySelectorAll('img');
    imageElements.forEach((img) => {
      if (img.src) {
        imageLinks.push(img.src);  // Extract the image source URL
      }
    });
  }
  return imageLinks;
}

// Function to extract attachments from the email
function extractAttachments() {
  const attachments = [];
  const attachmentElements = document.querySelectorAll('.aQh');
  attachmentElements.forEach((element) => {
    const attachmentName = element.querySelector('.aSH') ? element.querySelector('.aSH').innerText : 'Unknown Attachment';
    const attachmentLink = element.querySelector('a') ? element.querySelector('a').href : '';
    if (attachmentLink && attachmentName) {
      attachments.push({
        name: attachmentName,
        url: attachmentLink
      });
    }
  });
  return attachments;
}

// Function to extract email identifier (e.g., thread ID or subject)
function extractEmailId() {
  const emailSubjectElement = document.querySelector('.hP');  // Usually the email subject is in .hP
  const emailThreadIdElement = emailSubjectElement.getAttribute('data-thread-perm-id'); // Thread ID for unique identification

  // Return the thread ID or email subject (preferably thread ID as it's unique)
  if (emailThreadIdElement) {
    return emailThreadIdElement;
  } else {
    console.log('No thread identifier');
    return null;
  }
}

// Function to handle email content extraction
function handleEmail() {
  const emailText = extractEmailText();
  const urls = extractUrls();  // Extract URLs from the email body
  const imageLinks = extractImageLinks();  // Extract image URLs
  const attachments = extractAttachments();
  const emailId = extractEmailId();

  if (emailId && emailId !== lastProcessedEmailId) {
    // Update the last processed email ID to the current one
    lastProcessedEmailId = emailId;
    console.log('Email Text:', emailText);
    console.log('Extracted URLs:', urls);
    console.log('Extracted Image Links:', imageLinks);
    console.log('Extracted Attachments:', attachments);
    
    // Send the email content, URLs, image links, and attachments to your API endpoint
    sendSelectedContent(emailText, urls, imageLinks, attachments);
    
    // Send the email content, URLs, image links, and attachments to the background script or storage
    chrome.runtime.sendMessage({
      action: 'saveEmail',
      emailText: emailText,
      urls: urls,
      imageLinks: imageLinks,
      attachments: attachments
    });
  }
}

// Function to send selected content (email text, URLs, image links, attachments) to the Flask server
function sendSelectedContent(emailText, urls, imageLinks, attachments) {
  const data = {
    emailText: emailText,  // The email text content
    urls: urls,            // Extracted URLs
    imageLinks: imageLinks, // Extracted image URLs
    attachments: attachments // Extracted attachment details
  };

  // Send a POST request to the Flask server
  fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiToken}`  // Include the API token in the Authorization header
    },
    body: JSON.stringify(data)  // Convert the data to a JSON string
  })
  .then(response => response.json())
  .then(responseData => {
    // Handle the server's response
    console.log('Response from server:', responseData);
    if (responseData.message) {
      console.log('Content sent successfully: ' + responseData.message);
    } else if (responseData.error) {
      console.error('Error: ' + responseData.error);
    }
  })
  .catch(error => {
    console.error('Error sending data to the server:', error);
  });
}

// Function to check for email content periodically
function pollForEmailContent() {
  const emailBody = document.querySelector('.a3s.aiL'); // Check for email body
  if (emailBody) {
    handleEmail();  // Process the email content if found
  }
}

// Set a polling interval to check for email content every 5 seconds (5000ms)
const pollInterval = setInterval(pollForEmailContent, 5000);

window.addEventListener('load', () => { // Optional: Initial check right after the page loads
  pollForEmailContent();  // Do an initial check on load
});

// Handle potential page reloads or Gmail context changes by resetting the poll interval
window.addEventListener('beforeunload', () => {
  clearInterval(pollInterval); // Clear the previous polling interval if the page is unloading
});
