document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get('emailData', (data) => {
    const emailData = data.emailData;
    if (!emailData) {
      document.getElementById('email-content').textContent = '...Loading';
      return;
    }

    // 📝 Update Analysis Summary
    document.getElementById('spam-score').textContent = `${emailData.Spam}%`;
    document.getElementById('phishing-score').textContent = `${emailData.Phishing}%`;
    document.getElementById('llm-score').textContent = `${emailData.LLM}%`;
    document.getElementById('code-status').textContent = emailData.Code;
    document.getElementById('executables-status').textContent = emailData.Executables;

    
    const urlsSection = document.getElementById('urls-section'); // 🔗 Display URLs & Status
    urlsSection.innerHTML = '';  // Clear placeholder
    if (emailData.urls && Object.keys(emailData.urls).length > 0) {
      Object.entries(emailData.urls).forEach(([url, status]) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<a href="${url}" target="_blank">${url}</a> - <strong>${status}</strong>`;
        urlsSection.appendChild(listItem);
      });
    } else {
      urlsSection.innerHTML = '<li>No URLs found.</li>';
    }

    // // 📎 Display Attachments
    // const attachmentList = document.getElementById('attachment-list');
    // attachmentList.innerHTML = '';  // Clear placeholder
    // if (emailData.attachments && emailData.attachments.length > 0) {
    //   emailData.attachments.forEach(attachment => {
    //     const listItem = document.createElement('li');
    //     listItem.innerHTML = `<a href="${attachment.url}" target="_blank">${attachment.name}</a>`;
    //     attachmentList.appendChild(listItem);
    //   });
    // } else {
    //   attachmentList.innerHTML = '<li>No attachments.</li>';
    // }
  });
});
