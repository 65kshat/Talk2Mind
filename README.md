# 🧠 Talk2Mind

Talk2Mind is a multimodal mental wellbeing assessment system that combines questionnaire analysis, facial emotion recognition, and speech emotion recognition to provide a holistic understanding of an individual's emotional state.

The project was developed as part of an AI/ML internship and demonstrates the integration of Deep Learning, Computer Vision, Natural Language Processing concepts, and multimodal data fusion within an interactive Streamlit application.

---

## 📌 Features

### 📋 Questionnaire-Based Assessment

* DASS-inspired mental health questionnaire
* Evaluates stress, anxiety, and depression indicators
* Predicts mental wellbeing severity level
* Generates a questionnaire wellbeing score

### 😊 Facial Emotion Recognition

* Real-time webcam-based emotion detection
* Uses a deep learning model trained on facial expression datasets
* Detects emotions such as:

  * Happy
  * Sad
  * Angry
  * Fearful
  * Disgust
  * Surprised
  * Neutral

### 🎙️ Speech Emotion Recognition

* Records and analyzes user speech
* Extracts:

  * MFCC Features
  * RMS Energy
  * Zero Crossing Rate (ZCR)
* Uses an Attention-Based BiLSTM model for emotion classification
* Detects vocal emotional patterns across multiple emotion categories

### 🔄 Multimodal Fusion

* Combines outputs from:

  * Questionnaire Assessment
  * Facial Emotion Recognition
  * Speech Emotion Recognition
* Generates an overall wellbeing score
* Provides personalized recommendations based on assessment results

---

## 🏗️ System Architecture

```text
User Input
│
├── Questionnaire Responses
├── Webcam Analysis
└── Speech Recording
        │
        ▼
Individual Models
│
├── Questionnaire Neural Network
├── Facial Emotion Recognition Model
└── Attention BiLSTM Speech Model
        │
        ▼
Fusion Engine
        │
        ▼
Final Wellbeing Assessment
        │
        ▼
Personalized Recommendations
```

---

## 🤖 Machine Learning Models

### 1. Questionnaire Model

* Framework: PyTorch
* Fully Connected Neural Network
* Mental wellbeing severity classification
* Outputs:

  * Normal
  * Mild
  * Moderate
  * Severe
  * Extremely Severe

### 2. Facial Emotion Model

* Deep Learning based image classification model
* Real-time webcam inference
* Emotion probability estimation

### 3. Speech Emotion Model

* Attention-Based Bidirectional LSTM
* Input Features:

  * 40 MFCCs
  * RMS Energy
  * Zero Crossing Rate
* Emotion Classes:

  * Neutral
  * Calm
  * Happy
  * Sad
  * Angry
  * Fearful
  * Disgust
  * Surprised

---

## 📂 Project Structure

```text
Talk2Mind/
│
├── Frontend/
│   ├── app.py
│   ├── webcam_page.py
│   ├── audio_page.py
│   ├── questionnaire_page.py
│   └── results_page.py
│
├── Models/
│   ├── Questionnaire_Model.pth
│   ├── Speech_Model_V2.pth
│   └── Visual_Model.pth
│
├── Notebooks/
│   ├── Audio_Training.ipynb
│   ├── Visual_Training.ipynb
│   ├── Questionaire_Modelling.ipynb
│   └── Fusion_Model.ipynb
│
├── Utils/
│
├── requirements.txt
└── README.md
```

---

## 📊 Datasets Used

### Facial Emotion Recognition

* FER2013 Dataset

### Speech Emotion Recognition

* RAVDESS Emotional Speech Dataset

### Questionnaire Assessment

* DASS-based Mental Health Dataset

**Note:** Datasets are not included in this repository due to GitHub file size limitations.

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/65kshat/Talk2Mind.git
cd Talk2Mind
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run Frontend/app.py
```

---

## 📈 Technologies Used

* Python
* PyTorch
* Streamlit
* OpenCV
* Librosa
* NumPy
* Pandas
* Scikit-Learn
* Matplotlib

---

## ⚠️ Disclaimer

This project is intended for educational and research purposes only.

Talk2Mind is not a medical diagnostic tool and should not be used as a substitute for professional mental health assessment, diagnosis, or treatment.

---

## 🚀 Future Improvements

* Transformer-based speech emotion recognition
* Improved facial emotion recognition using larger datasets
* Continuous wellbeing tracking
* Cloud deployment
* User authentication and report history
* Multilingual speech analysis

---

## 👨‍💻 Author

**Akshat Sohni**

Artificial Intelligence & Machine Learning Enthusiast

GitHub: https://github.com/65kshat
