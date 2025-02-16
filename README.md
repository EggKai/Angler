<p align="center">
  <img src="angler-js/logo.png" alt="AnglerLogo"/>
</p>

```plaintext  
   __    _  _  ___  __    ____  ____ 
  /__\  ( \( )/ __)(  )  ( ___)(  _ \
 /(__)\  )  (( (_-. )(__  )__)  )   /
(__)(__)(_)\_)\___/(____)(____)(_)\_)
```
**Detecting Phishing Emails Using Machine Learning**
## **2. Team Members and Task Allocation**

- **Team Member 1: [Kelvin](https://github.com/WaterExecution)**  
  **Role**: Server (Web Server API as interface for ML)

- **Team Member 2: [AikKai](https://github.com/Eggkai)**  
  **Role**: Client (Extension to interface with Web Server API, Web Server API)

- **Team Member 3: [Hanyong](https://github.com/ForTheVibes)**  
  **Role**: Server (Integrate third-party services API)

- **Team Member 4: [Xaiver](https://github.com/Xyl0w)**  
  **Role**: Machine Learning (Develop, train, and optimize the phishing detection model)

- **Team Member 5: [Javier](https://github.com/java-0w)**  
  **Role**: Metrics/Performance Indicator (Generate reports and metrics for phishing detection accuracy and false positives)

- **Team Member 6: [Johan](https://github.com/johannybo1)**  
  **Role**: Data Processing/Feature Engineering (Cleaning, tokenization, handling missing values, metadata/URL analysis)

## **3. Problem Statement**

This project aims to build a classification model to determine whether an email is a phishing attempt or a legitimate message. By analyzing features of emails such as sender information, content, and embedded links, the model will help in identifying phishing emails to improve cybersecurity.

We aim to develop a Python-based web server with an extension client that addresses the issue of phishing emails. This solution will be beneficial for internet users by providing a service to detect malicious emails.

## **4. Proposed Solution**

Our solution will use a phishing detection model to analyze and process phishing emails, interfaced through a backend server. The primary goal is to achieve a high accuracy rate for the model and create an easy-to-use extension.


## **5. Project Plan and Timeline**

### **Phase 1: Planning and Setup (11-17 Jan 2025)**

- **Objectives**: Define project goals, finalize team roles, and set up development environments.
- **Tasks**:
    - Set up the Flask server and define API endpoints for interfacing with the ML model.
    - Research third-party services (e.g., Gmail API, OAuth) and plan integration.
    - Define the structure and functionality of the Chrome extension.
    - Gather and preprocess phishing/legitimate email datasets.
    - Define key metrics for evaluating phishing detection (e.g., accuracy, false positives).
    - Design the initial architecture of the ML model and evaluation framework.

- **Deliverables**:
    - Finalized project plan.
    - Development environments and repositories set up.
    - Basic API endpoint and dataset procurement.

### **Phase 2: Development (18-31 Jan 2025)**

- **Objectives**: Develop individual components and achieve integration for the progressive report.
- **Tasks**:
    - **Team Member 1**: Implement Malware Detection. Train ML model using dataset. Evaluate initial performance (e.g., precision, recall, F1 score). 
    - **Team Member 2**: Implement LLM Detection. Train ML model using dataset. Evaluate initial performance (e.g., precision, recall, F1 score). 
    - **Team Member 3**: Develop the content script to extract email data from Gmail. Build Flask API endpoints for receiving email data and returning detection results. Test API integration with mock data. 
    - **Team Member 4**: Train the ML model using the dataset and save it as a pickle file. Evaluate initial performance (e.g., precision, recall, F1 score). 
    - **Team Member 5**: Generate preliminary reports on detection accuracy using test data. Visualize initial metrics (e.g., confusion matrix, precision/recall curve).
    - **Team Member 6**: Implement Malicious URL Detection. Train ML model using dataset. Evaluate initial performance (e.g., precision, recall, F1 score). 

- **Deliverables**:
    - Progressive report with initial results.
    - Functional Flask API connected to the Chrome extension/Client.
    - Initial trained ML model.

### **Phase 3: Testing and Optimization (1-10 Feb 2025)**

- **Objectives**: Conduct thorough testing of individual components under various conditions. Optimize system performance, including ML models, API response times, and UI interactions. Integrate all components into a fully functional system. 
- **Tasks**:
    - **Team Member 1**: Test the malware detection module with different malware samples and benign files. Optimize the model by adjusting parameters and feature selection. Analyze detection errors and improve precision-recall balance. 
    - **Team Member 2**: Test the LLM detection model against real-world scenarios and refine it based on performance. Improve data set quality by adding more representative training data. Tune model parameters to reduce false positives and false negatives. 
    - **Team Member 3**: Validate the email extraction script with real Gmail data while ensuring compliance with security and privacy standards. Refine API request-response handling for robustness. Implement offline client for Angler Integrate models with to work with API Integrate API with external APIs for additional accuracy. 
    - **Team Member 4**: Re-train the ML model based on feedback from initial evaluation. Incorporate new phishing patterns identified during testing. Optimize the model’s memory and computation efficiency for better deployment. 
    - **Team Member 5**: Generate and analyze detailed performance reports (e.g., ROC curve, confusion matrix, precision-recall curve). Compare initial vs. optimized model performance. Summarize test results to identify improvement areas for final refinement. 
    - **Team Member 6**: Evaluate the malicious URL detection module using newly collected datasets. Implement fallback mechanisms for cases where predictions are uncertain. Improve feature extraction and selection for higher detection accuracy. 

- **Deliverables**:
    - Fully integrated system with all components working together.
    - Optimized ML models with improved accuracy and efficiency.
    - Refined Flask API ensuring reliable communication with the Chrome extension/Client.
    - Detailed test reports highlighting improvements and remaining challenges.


### **Phase 4: Finalization (11-16 Feb 2025)**

- **Objectives**:
    - Complete the final report with comprehensive documentation and findings.
    - Prepare source code and supporting materials for submission.
    - Create a demo video to showcase the system in action.

- **Tasks**:
    - **Team Member 1**: Document the malware detection implementation and key findings. Explain performance metrics and optimizations applied.
    - **Team Member 2**: Detail the LLM detection approach, including dataset preparation and model refinements. Discuss integration challenges and solutions. 
    - **Team Member 3**: Provide a technical overview of the email extraction process and API development. Document security considerations for handling Gmail data. 
    - **Team Member 4**: Describe the ML model training and improvements, including feature selection strategies. Highlight key optimizations and how they impacted performance. 
    - **Team Member 5**: Create visual representations of model performance (graphs, confusion matrices, etc.). Summarize detection results and overall system effectiveness. 
    - **Team Member 6**: Analyze the malicious URL detection model’s success rate and limitations. Propose future improvements and areas for expansion. 

- **Deliverables**:
    - Final report (due 16 Feb 2025, 11:59 PM).
    - Source code submission.
    - Presentation/demo video showcasing the project (due 16 Feb 2025, 11:59 PM).
    - Peer evaluation forms (if needed).

## **7. Installation Instructions**

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd phishing-email-detection
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask server:
    ```bash
    python main.py
    ```

4. Access the API at `http://_________:5000`.

---

Below is a simple diagram illustrating the flow of communication between the components of the system:
```plaintext
+---------------+          +---------------------+          +-----------------------+
|               |  HTTPS   |                     |          |                       |
|  Browser      +<-------->+    Web Server API   +<-------->+   Machine Learning    |
|  Extension    |          |       (Flask)       |          |         Model         |
|   (JS)        |          |                     |          |                       |
+---------------+          +---------------------+          +-----------------------+
```

As well as the file structure
```plaintext
Angler/
│
├── main.py                   # Flask application to run the server
├── requirements.txt         # Project dependencies
├── models/                  # Directory to store trained machine learning models
│   └── phishing_classifier.pkl  # Pre-trained model file
├── angler-js/              # Chrome extension source code
│   ├── . . .
│   ├── content.js           # Script to extract email data from the page
│   ├── . . .
│   └── manifest.json        # Extension configuration
├── server/                  # Web Server API
│   └── . . .
└── README.md                # Project documentation
```
### **8. Contributing**

Feel free to fork the repository and contribute by submitting issues and pull requests.

### **9. License**

This project is licensed under the MIT License.

---
