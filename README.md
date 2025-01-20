```plaintext  
   __    _  _  ___  __    ____  ____ 
  /__\  ( \( )/ __)(  )  ( ___)(  _ \
 /(__)\  )  (( (_-. )(__  )__)  )   /
(__)(__)(_)\_)\___/(____)(____)(_)\_)
```

## **Angler**
**Detecting Phishing Emails Using Machine Learning**

## **2. Team Members and Task Allocation**

- **Team Member 1: [Kelvin](https://github.com/WaterExecution)**  
  **Role**: Server (Web Server API as interface for ML)

- **Team Member 2: [AikKai](https://github.com/Eggkai)**  
  **Role**: Client (Extension to interface with Web Server API, Web Server API)

- **Team Member 3: Hanyong**  
  **Role**: Server (Integrate third-party services API)

- **Team Member 4: [Xaiver](https://github.com/Xyl0w)**  
  **Role**: Machine Learning (Develop, train, and optimize the phishing detection model)

- **Team Member 5: [Javier](https://github.com/java-0w)**  
  **Role**: Metrics/Performance Indicator (Generate reports and metrics for phishing detection accuracy and false positives)

- **Team Member 6: Johan**  
  **Role**: Data Processing/Feature Engineering (Cleaning, tokenization, handling missing values, metadata/URL analysis)

## **3. Problem Statement**

This project aims to build a classification model to determine whether an email is a phishing attempt or a legitimate message. By analyzing features of emails such as sender information, content, and embedded links, the model will help in identifying phishing emails to improve cybersecurity.

We aim to develop a Python-based web server with an extension client that addresses the issue of phishing emails. This solution will be beneficial for internet users by providing a service to detect malicious emails.

## **4. Proposed Solution**

Our solution will use a phishing detection model to analyze and process phishing emails, interfaced through a backend server. The primary goal is to achieve a high accuracy rate for the model and create an easy-to-use extension.

**Python Libraries**: 
- NumPy, Pandas, Matplotlib
- TensorFlow, Scikit-learn, Pytorch, NLTK
- Flask (for API development)

## **5. Data**

**Type of Data**: CSV files

**Data Sources**:  
1. [Phishing Emails Dataset by SubhaJournal](https://www.kaggle.com/datasets/subhajournal/phishingemails)  
2. [Web Page Phishing Detection Dataset](https://www.kaggle.com/datasets/manishkc06/web-page-phishing-detection)  
3. [Phishing Email Dataset by NaserAbdullahAlam](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)  
4. [Phishing Dataset for Machine Learning](https://www.kaggle.com/datasets/shashwatwork/phishing-dataset-for-machine-learning)  
5. [Phishing Paper1 Dataset](https://www.kaggle.com/datasets/akashsurya156/phishing-paper1)  
6. [Enron Email Dataset](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset)

## **6. Project Plan and Timeline**

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
    - **Team Member 1**: Build Flask API endpoints for receiving email data and returning detection results. Test API integration with mock data.
    - **Team Member 2**: Integrate Gmail API or other third-party email services for secure data access. Implement OAuth authentication.
    - **Team Member 3**: Develop the content script to extract email data from Gmail. Create the logic for communicating with the Flask API.
    - **Team Member 4**: Train the ML model using the dataset and save it as a pickle file. Evaluate initial performance (e.g., precision, recall, F1 score).
    - **Team Member 5**: Generate preliminary reports on detection accuracy using test data. Visualize initial metrics (e.g., confusion matrix, precision/recall curve).
    - **Team Member 6**: Optimize the ML model by tuning hyperparameters. Implement logic to reduce false positives/negatives.

- **Deliverables**:
    - Progressive report with initial results.
    - Functional Flask API connected to the Chrome extension/Client.
    - Initial trained ML model.

### **Phase 3: Testing and Optimization (1-10 Feb 2025)**

- **Objectives**: Test individual components, optimize performance, and integrate all parts.
- **Tasks**:
    - **Team Member 1**: Test the Flask API under different scenarios and handle edge cases. Optimize server response times and error handling.
    - **Team Member 2**: Validate Gmail API integration with real email accounts. Ensure secure handling of sensitive email data.
    - **Team Member 3**: Test the Chrome extension on multiple webmail platforms. Debug and improve the user interface.
    - **Team Member 4**: Re-train the ML model with feedback from initial tests. Add phishing patterns identified during integration testing.
    - **Team Member 5**: Generate detailed reports on metrics (e.g., ROC curve, false positive rate). Prepare performance summaries for the final report.
    - **Team Member 6**: Validate the model's performance on new datasets. Implement fallback mechanisms for ambiguous predictions.

- **Deliverables**:
    - Fully integrated system.
    - Optimized ML model with detailed performance reports.
    - Polished Chrome extension/Client.

### **Phase 4: Finalization (11-16 Feb 2025)**

- **Objectives**: Complete the final report, create a demo video, and prepare source code for submission.
- **Tasks**:
    - **Team Member 1**: Document API design and usage in the final report.
    - **Team Member 2**: Write about third-party API integration and challenges.
    - **Team Member 3**: Document the extension's functionality and UI features.
    - **Team Member 4**: Describe the ML model training process and improvements made.
    - **Team Member 5**: Add detailed visualizations and metrics to the final report.
    - **Team Member 6**: Summarize model performance, including success rates and limitations.

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

This project is licensed under the ___ License.

---
