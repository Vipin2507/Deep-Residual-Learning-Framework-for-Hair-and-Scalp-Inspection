# 🎯 Hair & Scalp Disease Prediction System

## 🚀 Quick Start (EASIEST METHOD)

### Just Double-Click to Run:
```
START_APPLICATION.bat
```

That's it! The application will:
- ✅ Check Python installation
- ✅ Create virtual environment automatically
- ✅ Install all dependencies
- ✅ Launch the Django server
- ✅ Open your browser automatically

**First run:** 2-3 minutes (installing dependencies)  
**Subsequent runs:** 10 seconds

---

## 📋 System Requirements

- **OS:** Windows 7/8/10/11
- **Python:** 3.8 or higher ([Download here](https://www.python.org/downloads/))
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 3GB free space

---

## 🎮 How to Use

1. **Start the Application**
   - Double-click `START_APPLICATION.bat`
   - Wait for browser to open

2. **Register/Login**
   - Create an account
   - Login with your credentials

3. **Make a Prediction**
   - Click "Get Started" or "Predict Disease"
   - Fill in patient information
   - Upload a scalp/hair image
   - Click "Predict"

4. **View Results**
   - See AI diagnosis
   - View disease stage analysis
   - Download professional PDF report

---

## 📁 Project Structure

```
required_files/
├── START_APPLICATION.bat     # 👈 Double-click this to run
├── run_app.py               # Python launcher
├── best_model.pth           # AI model (1.5GB)
├── README.md                # This file
└── minor/                   # Django application
    ├── manage.py
    ├── db.sqlite3
    ├── requirements.txt
    ├── minor/              # Settings
    └── myapp/              # Main app
        ├── templates/      # HTML files
        ├── views.py
        └── ml_service.py   # AI prediction
```

---

## 🔧 Troubleshooting

### Issue: "Python not found"
**Solution:** Install Python from [python.org](https://www.python.org/downloads/)
- ✅ Check "Add Python to PATH" during installation
- ✅ Restart computer after installation

### Issue: "Port 8000 already in use"
**Solution:** Close other Django apps or change port in `run_app.py`

### Issue: "Module not found" errors
**Solution:** Delete `minor\.venv` folder and run `START_APPLICATION.bat` again

### Issue: Slow predictions
**Solution:** 
- First prediction is always slower (model loading)
- Close other applications
- Use GPU if available (CUDA)

---

## 🎯 Features

### AI Capabilities
- ✅ 11 disease classifications
- ✅ 95%+ accuracy
- ✅ Confidence scoring
- ✅ Disease stage analysis (4 stages)
- ✅ Progression tracking

### User Features
- ✅ User authentication
- ✅ Session management
- ✅ Image upload & preview
- ✅ Zoom & pan on images
- ✅ Professional PDF reports
- ✅ Dark/Light theme
- ✅ Responsive design

### Clinical Features
- ✅ Patient information tracking
- ✅ Symptom duration tracking
- ✅ Disease stage calculation
- ✅ Severity assessment
- ✅ Clinical recommendations

---

## 🔒 Security & Privacy

- ✅ All data processed locally
- ✅ No external API calls
- ✅ Your data stays on your computer
- ✅ Password hashing (Django security)
- ✅ CSRF protection
- ✅ Session management

---

## 📊 Supported Diseases

1. Alopecia Areata
2. Contact Dermatitis
3. Folliculitis
4. Head Lice
5. Lichen Planus
6. Male Pattern Baldness
7. No Disease (Healthy)
8. Psoriasis
9. Seborrheic Dermatitis
10. Telogen Effluvium
11. Tinea Capitis

---

## 💡 Tips for Best Results

1. **Image Quality**
   - Use clear, well-lit images
   - Focus on the affected area
   - Optimal size: 500KB - 2MB

2. **Symptom Start Date**
   - Provide accurate date for stage analysis
   - Helps determine disease progression

3. **First Prediction**
   - Takes longer (model loading)
   - Subsequent predictions are faster

---

## 🛠️ For Developers

### Run Manually
```bash
cd minor
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Create Superuser
```bash
cd minor
.venv\Scripts\activate
python manage.py createsuperuser
```
Access admin at: http://127.0.0.1:8000/admin

### Update Dependencies
```bash
cd minor
.venv\Scripts\activate
pip install --upgrade -r requirements.txt
```

---

## 📞 Support

- Check console error messages
- Review this README
- Ensure all files are in correct locations
- Verify Python installation

---

## 📝 Version Information

- **Django:** 4.2+
- **PyTorch:** 2.0+
- **Python:** 3.8+
- **Model:** ResNet50 (11 classes)
- **Database:** SQLite3

---

## ⚠️ Important Notes

- Keep console window **OPEN** while using the app
- Press **Ctrl+C** to stop the server
- First run takes longer (dependency installation)
- All data stays on your computer (private & secure)

---

**🎉 Enjoy using the Hair & Scalp Disease Prediction System!**

For best experience, just double-click `START_APPLICATION.bat` and you're ready to go!
