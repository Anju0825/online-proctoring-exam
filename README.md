![IMG_20240826_211132](https://github.com/user-attachments/assets/c216c446-d48e-4fb7-99a7-928260f27a1e)# AI-Based Online Proctoring System

A real-time AI-powered online proctoring system built using **Flask** and **OpenCV** to monitor candidates during online examinations and detect suspicious activities such as face absence, multiple faces, and tab switching.

---

## Features

* **Face Detection** – Detects presence of candidate using webcam (Haar Cascade)
* **Multiple Face Detection** – Flags when more than one face is detected
* **Face Absence Alert** – Detects when candidate leaves the screen
* **Tab Switching Detection** – Prevents cheating via tab switching
* **Exam Timer** – Auto submission after time ends
* **Image Capture** – Captures evidence for suspicious activities
* **Admin Dashboard** – View logs, alerts, and captured images
* **User Authentication** – Secure login system using Flask-Login

---

## Tech Stack

**Frontend:**

* HTML, CSS, JavaScript, Bootstrap

**Backend:**

* Python, Flask

**Database:**

* SQLite (SQLAlchemy ORM)

**Libraries & Tools:**

* OpenCV (Computer Vision)
* NumPy
* Flask-Login
* Jinja2
* Git & GitHub

---

## How It Works

1. User logs into the system
2. Exam starts with webcam access
3. OpenCV continuously monitors:

   * Face presence
   * Number of faces
4. JavaScript tracks:

   * Tab switching
   * Window focus
5. Suspicious activities are:

   * Logged in database
   * Captured as images
6. Admin can review all logs from dashboard
 

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-proctoring-system.git
cd ai-proctoring-system
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000/
```

---

## Project Structure

```
ai-proctoring-system/
│
├── static/              # CSS, JS, Images
├── templates/           # HTML Templates
├── models/              # Database models
├── routes/              # Flask routes
├── utils/               # Detection logic (OpenCV)
├── app.py               # Main Flask app
├── requirements.txt
└── README.md
```

---

## Future Improvements

* 🎤 Audio detection for background noise
* 🤖 AI-based behavior analysis (eye tracking)
* ☁️ Cloud storage for logs & images
* 📈 Advanced analytics dashboard
* 📧 Email alerts for suspicious activity

---

## Use Cases

* Online examinations
* Remote hiring tests
* Certification platforms
* E-learning platforms

---

## Contribution

Feel free to fork the repository and submit pull requests.

---

## Contact

**Anjali Mishra**
📩 [go4anjali08@gmail.com](mailto:go4anjali08@gmail.com)
🔗 GitHub: https://github.com/Anju0825
🔗 LinkedIn: https://linkedin.com/in/anjali-mishra-792b77205

---

⭐ If you found this project useful, consider giving it a star!

