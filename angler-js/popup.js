function createCircleChart(id, percent) {
  Circles.create({
    id: `circles-${id}`,
    maxValue: 100,
    value: percent,
    radius: 30,
    width: 6,
    text: function (value) { return value + '%'; },
    colors: ['grey', percent > 60 ? 'red ' : 'green'],
    duration: 2000,
    wrpClass: 'circles-wrp',
    textClass: 'circles-text',
    valueStrokeClass: 'circles-valueStroke',
    maxValueStrokeClass: 'circles-maxValueStroke',
    styleWrapper: true,
    styleText: true
  });
}
function updateLoadingBar(progress) {
  const loadingProgress = document.getElementById('loading-progress');
  if (loadingProgress) {
    loadingProgress.style.width = `${progress}%`;
  }
}

function updateWebpage() {
  const loadingBar = document.getElementById('loading-bar');
  if (loadingBar) {
    loadingBar.hidden = false; //show progress bar
  }

  chrome.storage.local.get('emailData', (data) => {
    const emailData = data?.emailData;

    // If no data, show the loading bar at 90%
    if (!emailData) {
      updateLoadingBar(90);  // Set the progress of the loading bar
      document.getElementById('loading-text').textContent = 'Loading...';
      return;
    }

    // Check if any required fields are missing, and if so, show the loading bar at 95%
    const requiredFields = ['Spam', 'Phishing', 'LLM', 'urls', 'Code', 'Executables'];
    const missingFields = requiredFields.filter(field => !(field in emailData));
    if (missingFields.length > 0) {
      updateLoadingBar(95);  // Update loading bar progress to 60%
      document.getElementById('loading-text').textContent = 'Loading...';
      return;
    }
    updateLoadingBar(99);  // Set the progress to 99% to indicate almost complete

    // 🤡Remove the loading indicator
    const loadingContainer = document.getElementById('loading-container');
    if (loadingContainer) {
      loadingContainer.style.display = 'none';  // Hide the loading container once loading is done
    }
    const emailContent = document.getElementById('email-content');
    if (emailContent) {
      emailContent.hidden = false;  // Show the email content
    }

    // 📝 Update Analysis Summary
    // document.getElementById('spam-score').textContent = `${emailData?.Spam}%`;
    // document.getElementById('phishing-score').textContent = `${emailData?.Phishing}%`;
    // document.getElementById('llm-score').textContent = `${emailData?.LLM}%`;
    document.getElementById('code').textContent = `${emailData?.Code ?? 'No Code Files'}`;
    document.getElementById('executables').textContent = `${emailData?.Executables ?? "No Executable Files"}`;


    const urlsSection = document.getElementById('urls-section'); // 🔗 Display URLs & Status
    urlsSection.innerHTML = '';  // Clear placeholder
    if (emailData.urls && Object.keys(emailData.urls).length > 0) {
      Object.entries(emailData.urls).forEach(([url, status]) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<a ${!status?`href="${url}"`:''} target="_blank">${url}</a> - <strong>${status?'Potentially Unsafe':'Safe'}</strong>`; //we dont want the link to be clickable if it is safe
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
}

document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get('busy', (data) => {
    if (!data.busy) {
      const loadingBar = document.getElementById('loading-bar');
      if (loadingBar) {
        loadingBar.hidden = true;  // Hide progress bar
      }
      document.getElementById('loading-text').textContent = 'Open a Email to analyse';
      return;
    }
    updateWebpage();
  });
});

// 🟢 Detect changes in chrome.storage.local and update automatically
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local' && changes.emailData) {
    console.log('emailData changed:', changes.emailData.newValue);
    updateWebpage();  // Re-run webpage update when emailData changes
  }
});