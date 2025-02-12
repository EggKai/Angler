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

// Function to download and convert attachment to Base64
async function fetchAttachmentAsBase64(url, retries = 5, delay = 1000) {
  for (let i = 0; i < retries; i++) {
  try {
      const response = await fetch(url, {
        credentials: "include", headers: {
          "User-Agent": navigator.userAgent, // Mimic a real browser request
          "Referer": "https://mail.google.com", // Gmail's origin
          "Accept": "*/*"
        }, redirect: "follow"
      });
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const blob = await response.blob();
    return new Promise((resolve) => {
      const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
      reader.readAsDataURL(blob);
    });
  } catch (error) {
      console.error(`Attempt ${i + 1} failed:`, error);
      if (i < retries - 1) await new Promise((res) => setTimeout(res, delay)); // Wait before retrying
    }
  }
    return null;
  }

// Function to download and convert attachment to Text
async function fetchAttachmentAsText(url, retries = 5, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, {
        credentials: "include", headers: {
          "User-Agent": navigator.userAgent, // Mimic a real browser request
          "Referer": "https://mail.google.com", // Gmail's origin
          "Accept": "*/*"
        }, redirect: "follow"
      });
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      console.log(response);
      console.log(response.textContent);
      // const blob = await response.blob();
      // return new Promise((resolve) => {
      //   const reader = new FileReader();
      //   console.log(reader.result);
      //   reader.onloadend = () => resolve(btoa(reader.result));;
      //   reader.readAsText(blob);
      // });
    } catch (error) {
      console.error(`Attempt ${i + 1} failed:`, error);
      if (i < retries - 1) await new Promise((res) => setTimeout(res, delay)); // Wait before retrying
    }
  }
  return null;
}

// Function to extract attachments from the email
async function extractAttachments() {
  const attachments = [];
  const attachmentElements = document.querySelectorAll('div .aQH > .aZo');
  // console.log(attachmentElements);
  for (const element of attachmentElements) {
    const attachmentLink = element.querySelector('a') ? element.querySelector('a').href : '';
    const attachmentName = element.querySelector('a > span.a3I') ? element.querySelector('a > span.a3I').innerText : '';
    console.log(attachmentName, attachmentLink);
    if (attachmentLink && attachmentName) {
      if (['js', 'ps1', 'c', 'rs', 'sh', 'py', 'txt', 'csv'].includes(attachmentName.split('.').pop().toLowerCase())) {
        // console.log(attachmentName, attachmentName.split('.').pop().toLowerCase());
        const textData = await fetchAttachmentAsText(attachmentLink);
        if (textData) {
          attachments.push({
            name: attachmentName,
            base64: textData,
            mimeType: 'text/plain' //Plaintext MIMEType
          });
        }
      } else {
      const base64Data = await fetchAttachmentAsBase64(attachmentLink);
      if (base64Data) {
        attachments.push({
          name: attachmentName,
          base64: base64Data,
          mimeType: 'application/octet-stream' // Default MIME type, can be adjusted if needed
        });
      }
    }

    }
  }
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
async function handleEmail() {
  chrome.runtime.sendMessage({
    action: 'busy',
  });
  const emailText = extractEmailText();
  const urls = extractUrls();  // Extract URLs from the email body
  const imageLinks = extractImageLinks();  // Extract image URLs
  const emailId = extractEmailId();

  if (emailId && emailId !== lastProcessedEmailId) {
    // Update the last processed email ID to the current one
    lastProcessedEmailId = emailId;

    // Send the email content, URLs, image links, and attachments to your API endpoint
    const attachments = await extractAttachments(); // Wait for attachment data
    sendSelectedContent(emailText, urls, imageLinks, attachments);
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
  console.log(data)
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
      chrome.runtime.sendMessage({
        action: 'saveEmail',
        emailData: responseData,  // Save the server's response
      });
    })
    .catch(error => {
      console.error('Error sending data to the server:', error);
    });
}

// Set up MutationObserver to watch for changes in the DOM
const observer = new MutationObserver((mutationsList) => {
  for (const mutation of mutationsList) {
    if (mutation.type === 'childList') {
      // Check if the .a3s.aiL element is added or removed
      const emailBody = document.querySelector('.a3s.aiL');
      if (emailBody) {

        handleEmail();  // Process the email content if found
      } else {
        chrome.runtime.sendMessage({
          action: 'clearEmail',
        });
      }
    }
  }
});

// Configure the MutationObserver to watch for the addition/removal of child elements
const config = { childList: true, subtree: true };
observer.observe(document.body, config);

// Handle potential page reloads or Gmail context changes by disconnecting the observer
window.addEventListener('beforeunload', () => {
  observer.disconnect(); // Stop observing when the page is unloading
});

window.addEventListener('load', () => {
  const emailBody = document.querySelector('.a3s.aiL');
  if (emailBody) {
    handleEmail();  // Initial check on page load if the email body exists
  }
});
