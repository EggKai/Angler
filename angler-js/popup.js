function createCircleChart(id, percent, threshold) {
  Circles.create({
    id: `circles-${id}`,
    maxValue: 100,
    value: percent,
    radius: 30,
    width: 6,
    text: function (value) { return value + '%'; },
    colors: ['#d3d3d3', percent > threshold ? 'red ' : 'green'],
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
    loadingBar.hidden = false; // Show progress bar
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
    const requiredFields = ['Spam', 'Phishing', 'LLM', 'urls', 'attachments', 'verdict'];
    const missingFields = requiredFields.filter(field => !(field in emailData));
    if (missingFields.length > 0) {
      updateLoadingBar(95);  // Update loading bar progress to 60%
      document.getElementById('loading-text').textContent = 'Loading...';
      return;
    }
    updateLoadingBar(99);  // Set the progress to 99% to indicate almost complete

    // Remove the loading indicator
    const loadingContainer = document.getElementById('loading-container');
    if (loadingContainer) {
      loadingContainer.style.display = 'none';  // Hide the loading container once loading is done
    }
    const toggleButton = document.getElementById('toggle-details-button');
    if (toggleButton) {
      toggleButton.hidden = false; // Show progress bar
    }
    // Display the verdict
    const verdictContainer = document.getElementById('verdict-container');
    const verdictText = document.getElementById('verdict-text');
    if (verdictContainer && verdictText) {
      verdictContainer.hidden = false;
      verdictText.textContent = emailData.verdict?"Malicious":"Benign";
      verdictText.className = `${emailData.verdict?'red-text':'green-text'}`
    }

    // Update Analysis Summary
    const urlsSection = document.getElementById('urls-section'); // Display URLs & Status
    urlsSection.innerHTML = '';  // Clear placeholder
    if (emailData.urls && Object.keys(emailData.urls).length > 0) {
      Object.entries(emailData.urls).forEach(([url, status]) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<a ${!status?`href="${url}"`:''} target="_blank">${url}</a> - <strong class="${status?'red-text':'green-text'}">${status?'Potentially Unsafe':'Safe'}</strong>`; //we dont want the link to be clickable if it is safe
        urlsSection.appendChild(listItem);
      });
    } else {
      urlsSection.innerHTML = '<li>No URLs found.</li>';
    }
    createCircleChart('phishing', emailData.Phishing, 84)
    createCircleChart('spam', emailData.Spam, 96)
    createCircleChart('llm', emailData.LLM, 50)

    // Display Attachments
    const attachmentList = document.getElementById('attachment-list');
    attachmentList.innerHTML = '';  // Clear placeholder
    if (emailData.attachments && Object.keys(emailData.attachments).length > 0) {
      Object.entries(emailData.attachments).forEach(([attachmentname, status]) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `${attachmentname} - <strong class="${status?'red-text':'green-text'}">${status?'Potentially Unsafe':'Safe'}</strong>`; //we dont want the link to be clickable if it is safe
        attachmentList.appendChild(listItem);
      });
    } else {
      attachmentList.innerHTML = '<li>No attachments.</li>';
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get('busy', (data) => {
    if (!data.busy) {
      const loadingBar = document.getElementById('loading-bar');
      if (loadingBar) {
        loadingBar.hidden = true;  // Hide progress bar
      }
      if (loadingBar) {
        loadingBar.hidden = true;  // Hide progress bar
      }
      document.getElementById('loading-text').textContent = 'Open an Email to analyse';
      return;
    }
    updateWebpage();
  });

  // Add event listener for the toggle details button
  const toggleDetailsButton = document.getElementById('toggle-details-button');
  if (toggleDetailsButton) {
    toggleDetailsButton.addEventListener('click', () => {
      const emailContent = document.getElementById('email-content');
      if (emailContent) {
        emailContent.hidden = !emailContent.hidden;
        toggleDetailsButton.textContent = emailContent.hidden ? 'Show Details' : 'Hide Details';
      }
    });
  }
});

// Detect changes in chrome.storage.local and update automatically
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local' && changes.emailData) {
    console.log('emailData changed:', changes.emailData.newValue);
    updateWebpage();  // Re-run webpage update when emailData changes
  }
});