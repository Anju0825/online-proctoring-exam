import os
import cv2
import base64
import json
import datetime
from flask import Flask, render_template, redirect, url_for, request, Response, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'proctor-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- DATABASE MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    face_enrolled = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- PROCTORING LOGIC ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def log_violation(user_id, v_type, frame):
    log_dir = f"data_lake/logs/{user_id}"
    img_dir = f"data_lake/violations/{user_id}"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    img_path = f"{img_dir}/{timestamp}.jpg"
    cv2.imwrite(img_path, frame)
    log_path = f"{log_dir}/violations.json"
    entry = {"timestamp": timestamp, "type": v_type, "evidence": img_path}
    logs = []
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            try: logs = json.load(f)
            except: logs = []
    logs.append(entry)
    with open(log_path, 'w') as f:
        json.dump(logs, f, indent=4)

# --- ROUTES ---
@app.route('/')
def index(): return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        # PREVENT BIG ERROR: Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email is already registered. Please login.', 'warning')
            return redirect(url_for('register'))
            
        pw = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(name=request.form['name'], email=email, password=pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard(): return render_template('dashboard.html', user=current_user)

@app.route('/enroll_face', methods=['POST'])
@login_required
def enroll_face():
    data = request.json['image']
    img_data = base64.b64decode(data.split(',')[1])
    user_dir = f"data_lake/users/{current_user.id}"
    os.makedirs(user_dir, exist_ok=True)
    with open(f"{user_dir}/face.jpg", "wb") as f: f.write(img_data)
    current_user.face_enrolled = True
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/exam')
@login_required
def exam_page(): return render_template('exam.html')

@app.route('/submit_exam', methods=['POST'])
@login_required
def submit_exam():
    data = request.json
    score = data.get('score', 0)
    v_count = 0
    log_path = f"data_lake/logs/{current_user.id}/violations.json"
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            try: v_count = len(json.load(f))
            except: v_count = 0
    return jsonify({"status": "success", "score": score, "violations": v_count})

@app.route('/result')
@login_required
def result_page(): return render_template('result.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/video_feed')
@login_required
def video_feed():
    def gen():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        frame_skip = 0
        while True:
            success, frame = cap.read()
            if not success: break
            frame_skip += 1
            if frame_skip % 10 == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                if len(faces) != 1: log_violation(current_user.id, "Proctoring Alert", frame)
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        cap.release()
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)  