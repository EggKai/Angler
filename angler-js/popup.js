document.addEventListener('DOMContentLoaded', () => {
    chrome.storage.local.get('emailData', (data) => {
      const emailData = data.emailData;
  
      if (emailData) {
        // Display email text
        document.getElementById('email-text').textContent = emailData.emailText || 'No email text found.';
        
        // Display attachments
        const attachmentList = document.getElementById('attachment-list');
        emailData.attachments.forEach(attachment => {
          const listItem = document.createElement('li');
          listItem.textContent = `${attachment.name} - [Link](${attachment.url})`;
          attachmentList.appendChild(listItem);
        });
      } else {
        document.getElementById('email-content').textContent = 'No email data available.';
      }
    });
  });
  