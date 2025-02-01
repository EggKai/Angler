function createCircleChart(id, percent){
  Circles.create({
    id:                  `circles-${id}`,
    maxValue:            100,
    value:        percent,
    radius:       30,
    width:        6,
    text:                function(value){return value + '%';},
    colors:              ['grey', 'green'],
    duration:            500,
    wrpClass:            'circles-wrp',
    textClass:           'circles-text',
    valueStrokeClass:    'circles-valueStroke',
    maxValueStrokeClass: 'circles-maxValueStroke',
    styleWrapper:        true,
    styleText:           true
  });
}
document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get('busy', (data) => {
    if (!data.busy) {
      document.getElementById('email-content').textContent = 'Open a Email to analyse'; 
      return;
    }
  
  chrome.storage.local.get('emailData', (data) => {
    const emailData = data.emailData;
    if (!emailData) {
      //TODO: Loading Bar
      document.getElementById('email-content').textContent = 'Loading...'; 
    }
    // 📝 Update Analysis Summary
    // document.getElementById('spam-score').textContent = `${emailData?.Spam}%`;
    // document.getElementById('phishing-score').textContent = `${emailData?.Phishing}%`;
    // document.getElementById('llm-score').textContent = `${emailData?.LLM}%`;
    document.getElementById('code').textContent =  `${emailData.Code ?? 'No Code Files'}`;
    document.getElementById('executables').textContent =`${emailData.Executables ?? "No Executable Files"}`;
    
    
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
    createCircleChart('phishing', emailData.Phishing)
    createCircleChart('spam', emailData.Spam,)
    createCircleChart('llm', emailData.LLM)
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

});