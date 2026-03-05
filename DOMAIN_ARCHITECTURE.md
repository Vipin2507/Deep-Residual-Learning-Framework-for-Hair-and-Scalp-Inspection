# 🏗️ HAIR & SCALP DISEASE PREDICTION SYSTEM
## Complete Domain & Architecture Documentation

---

## 📊 SYSTEM ARCHITECTURE OVERVIEW

### High-Level System Diagram
```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER (Browser)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Desktop    │  │    Tablet    │  │    Mobile    │             │
│  │   Browser    │  │    Browser   │  │    Browser   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         │                  │                  │                      │
│         └──────────────────┼──────────────────┘                     │
│                            │                                         │
│                    HTTPS/SSL (Port 443)                             │
└────────────────────────────┼───────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Static Files (CDN)                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │  │
│  │  │   HTML   │  │   CSS    │  │    JS    │  │  Images  │    │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┼───────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      WEB SERVER LAYER                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Gunicorn (WSGI Server)                     │  │
│  │                    Workers: 4-8 processes                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┼───────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER (Django)                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      URL Dispatcher                           │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │   /home    │  │  /predict  │  │  /camera   │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      Middleware Stack                         │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │  Security  │  │    CORS    │  │   Session  │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      View Layer                               │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │   Views    │  │    API     │  │   Forms    │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┼───────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────┐
│   BUSINESS LOGIC     │  │    ML SERVICE        │  │   DATABASE   │
│                      │  │                      │  │              │
│  ┌────────────────┐ │  │  ┌────────────────┐ │  │  ┌────────┐  │
│  │ Authentication │ │  │  │  PyTorch Model │ │  │  │MongoDB │  │
│  │ Authorization  │ │  │  │  Preprocessing │ │  │  │        │  │
│  │ Validation     │ │  │  │  Inference     │ │  │  │ Users  │  │
│  │ Business Rules │ │  │  │  Post-process  │ │  │  │ Preds  │  │
│  └────────────────┘ │  │  └────────────────┘ │  │  │Sessions│  │
└──────────────────────┘  └──────────────────────┘  └──────────────┘
```

---


## 🌐 DOMAIN MODEL DIAGRAM

### Core Domain Entities
```
┌─────────────────────────────────────────────────────────────────┐
│                         USER DOMAIN                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                        User                               │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  - id: ObjectId                                          │  │
│  │  - username: String                                      │  │
│  │  - email: String (unique)                                │  │
│  │  - password_hash: String                                 │  │
│  │  - created_at: DateTime                                  │  │
│  │  - last_login: DateTime                                  │  │
│  │  - is_active: Boolean                                    │  │
│  │  - profile: Profile                                      │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  + register()                                            │  │
│  │  + login()                                               │  │
│  │  + logout()                                              │  │
│  │  + update_profile()                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            │ 1:1                                 │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      Profile                              │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  - user_id: Reference                                    │  │
│  │  - full_name: String                                     │  │
│  │  - date_of_birth: Date                                   │  │
│  │  - phone: String                                         │  │
│  │  - address: String                                       │  │
│  │  - preferences: Object                                   │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  + update()                                              │  │
│  │  + get_age()                                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ 1:N
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PREDICTION DOMAIN                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Prediction                            │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  - id: ObjectId                                          │  │
│  │  - user_id: Reference                                    │  │
│  │  - image_data: String (base64)                           │  │
│  │  - predicted_class: String                               │  │
│  │  - confidence: Float (0-1)                               │  │
│  │  - all_probabilities: Array[Float]                       │  │
│  │  - stage_info: StageInfo                                 │  │
│  │  - timestamp: DateTime                                   │  │
│  │  - metadata: Object                                      │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  + create()                                              │  │
│  │  + get_by_user()                                         │  │
│  │  + delete()                                              │  │
│  │  + generate_report()                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            │ 1:1                                 │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    StageInfo                              │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  - stage: String (Early/Moderate/Advanced)              │  │
│  │  - severity: String (Mild/Moderate/Severe)              │  │
│  │  - days_elapsed: Integer                                 │  │
│  │  - progression_rate: String                              │  │
│  │  - clinical_notes: String                                │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  + calculate_stage()                                     │  │
│  │  + get_recommendations()                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ N:1
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DISEASE DOMAIN                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      Disease                              │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  - id: ObjectId                                          │  │
│  │  - name: String                                          │  │
│  │  - description: String                                   │  │
│  │  - symptoms: Array[String]                               │  │
│  │  - causes: Array[String]                                 │  │
│  │  - treatments: Array[String]                             │  │
│  │  - prevention: Array[String]                             │  │
│  │  - severity_levels: Array[String]                        │  │
│  │  - image_url: String                                     │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  + get_info()                                            │  │
│  │  + get_all()                                             │  │
│  │  + search()                                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       SESSION DOMAIN                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      Session                              │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  - session_id: String (unique)                           │  │
│  │  - user_id: Reference                                    │  │
│  │  - data: Object                                          │  │
│  │  - created_at: DateTime                                  │  │
│  │  - expires_at: DateTime                                  │  │
│  │  - ip_address: String                                    │  │
│  │  - user_agent: String                                    │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  + create()                                              │  │
│  │  + validate()                                            │  │
│  │  + refresh()                                             │  │
│  │  + destroy()                                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 DATA FLOW DIAGRAM

### Complete Request-Response Flow
```
┌─────────────┐
│    USER     │
│  (Browser)  │
└──────┬──────┘
       │
       │ 1. Upload Image / Capture Photo
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (JavaScript)                       │
│  ┌────────────────────────────────────────────────────┐ │
│  │  1. Validate Image (size, format)                  │ │
│  │  2. Compress Image (if needed)                     │ │
│  │  3. Convert to Base64                              │ │
│  │  4. Show Loading Animation                         │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ 2. POST /predict
                       │    {image: base64, user_id: xxx}
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              DJANGO MIDDLEWARE                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  1. CSRF Token Validation                          │ │
│  │  2. Authentication Check                           │ │
│  │  3. CORS Headers                                   │ │
│  │  4. Rate Limiting                                  │ │
│  │  5. Request Logging                                │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ 3. Validated Request
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              DJANGO VIEW (predict_view)                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │  1. Extract image from request                     │ │
│  │  2. Decode base64 to image                         │ │
│  │  3. Validate image format                          │ │
│  │  4. Get user information                           │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ 4. Image Data
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              ML SERVICE (ml_service.py)                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │  PREPROCESSING                                      │ │
│  │  1. Resize to 224x224                              │ │
│  │  2. Normalize pixel values                         │ │
│  │  3. Convert to tensor                              │ │
│  │  4. Add batch dimension                            │ │
│  └────────────────────────────────────────────────────┘ │
│                       │                                  │
│                       │ 5. Preprocessed Tensor           │
│                       ▼                                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │  MODEL INFERENCE                                    │ │
│  │  1. Load model (best_model.pth)                    │ │
│  │  2. Set to evaluation mode                         │ │
│  │  3. Forward pass through network                   │ │
│  │  4. Apply softmax for probabilities                │ │
│  │  5. Get top prediction and confidence              │ │
│  └────────────────────────────────────────────────────┘ │
│                       │                                  │
│                       │ 6. Raw Predictions               │
│                       ▼                                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │  POST-PROCESSING                                    │ │
│  │  1. Map class index to disease name                │ │
│  │  2. Calculate stage information                    │ │
│  │  3. Format confidence score                        │ │
│  │  4. Prepare response data                          │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ 7. Prediction Results
                       │    {class: "Alopecia", confidence: 0.92}
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              DATABASE OPERATIONS                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │  1. Create prediction document                     │ │
│  │  2. Save to MongoDB                                │ │
│  │  3. Update user history                            │ │
│  │  4. Log prediction event                           │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ 8. Database Confirmation
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              DJANGO VIEW (Response)                      │
│  ┌────────────────────────────────────────────────────┐ │
│  │  1. Format response JSON                           │ │
│  │  2. Add metadata                                   │ │
│  │  3. Set response headers                           │ │
│  │  4. Return HTTP 200                                │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ 9. JSON Response
                       │    {success: true, prediction: {...}}
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (JavaScript)                       │
│  ┌────────────────────────────────────────────────────┐ │
│  │  1. Parse JSON response                            │ │
│  │  2. Hide loading animation                         │ │
│  │  3. Update UI with results                         │ │
│  │  4. Display prediction details                     │ │
│  │  5. Enable download PDF button                     │ │
│  │  6. Store in localStorage                          │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ 10. Display Results
                       │
                       ▼
┌─────────────┐
│    USER     │
│  (Sees      │
│   Results)  │
└─────────────┘
```

---


## 🗂️ PROJECT STRUCTURE DIAGRAM

### Complete Directory Tree
```
hair-scalp-detector/
│
├── 📁 .git/                          # Git version control
│
├── 📄 .gitignore                     # Git ignore rules
├── 📄 README.md                      # Project documentation
├── 📄 PRESENTATION_SCRIPT.md         # Presentation guide
├── 📄 DOMAIN_ARCHITECTURE.md         # This file
│
├── 📄 best_model.pth                 # Trained ML model (45MB)
├── 📄 HairScalpPredictor.spec        # PyInstaller spec
├── 📄 run_app.py                     # Application launcher
├── 📄 START_APPLICATION.bat          # Windows startup script
├── 📄 setup_mobile_app.bat           # Mobile setup script
│
├── 📁 frontend/                      # Static frontend files
│   ├── 📄 index.html                # Landing page
│   └── 📄 result.html               # Results page
│
├── 📁 minor/                         # Django project root
│   │
│   ├── 📄 manage.py                 # Django CLI tool
│   ├── 📄 requirements.txt          # Python dependencies
│   ├── 📄 requirements_production.txt # Production deps
│   ├── 📄 runtime.txt               # Python version
│   │
│   ├── 📁 minor/                    # Project settings
│   │   ├── 📄 __init__.py
│   │   ├── 📄 settings.py          # Development settings
│   │   ├── 📄 settings_production.py # Production settings
│   │   ├── 📄 urls.py              # Main URL routing
│   │   ├── 📄 wsgi.py              # WSGI configuration
│   │   └── 📄 asgi.py              # ASGI configuration
│   │
│   ├── 📁 myapp/                    # Main application
│   │   ├── 📄 __init__.py
│   │   ├── 📄 admin.py             # Admin panel config
│   │   ├── 📄 apps.py              # App configuration
│   │   ├── 📄 models.py            # Database models
│   │   ├── 📄 views.py             # View functions
│   │   ├── 📄 urls.py              # App URL routing
│   │   ├── 📄 forms.py             # Form definitions
│   │   ├── 📄 middleware.py        # Custom middleware
│   │   ├── 📄 ml_service.py        # ML integration
│   │   ├── 📄 tests.py             # Unit tests
│   │   │
│   │   ├── 📁 migrations/          # Database migrations
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 0001_initial.py
│   │   │
│   │   ├── 📁 static/              # Static files
│   │   │   ├── 📁 css/
│   │   │   │   ├── 📄 main.css
│   │   │   │   ├── 📄 responsive.css
│   │   │   │   └── 📄 dark-mode.css
│   │   │   │
│   │   │   ├── 📁 js/
│   │   │   │   ├── 📄 main.js
│   │   │   │   ├── 📄 camera.js
│   │   │   │   ├── 📄 prediction.js
│   │   │   │   └── 📄 pwa-install.js
│   │   │   │
│   │   │   ├── 📁 icons/           # PWA icons
│   │   │   │   ├── 📄 icon-72x72.png
│   │   │   │   ├── 📄 icon-96x96.png
│   │   │   │   ├── 📄 icon-128x128.png
│   │   │   │   ├── 📄 icon-144x144.png
│   │   │   │   ├── 📄 icon-152x152.png
│   │   │   │   ├── 📄 icon-192x192.png
│   │   │   │   ├── 📄 icon-384x384.png
│   │   │   │   └── 📄 icon-512x512.png
│   │   │   │
│   │   │   ├── 📁 images/
│   │   │   │   ├── 📄 logo.png
│   │   │   │   ├── 📄 hero-bg.jpg
│   │   │   │   └── 📄 disease-*.jpg
│   │   │   │
│   │   │   ├── 📄 manifest.json    # PWA manifest
│   │   │   ├── 📄 service-worker.js # Service worker
│   │   │   ├── 📄 browserconfig.xml
│   │   │   └── 📄 pwa-styles.css
│   │   │
│   │   └── 📁 templates/           # HTML templates
│   │       ├── 📄 base.html        # Base template
│   │       ├── 📄 home.html        # Homepage
│   │       ├── 📄 login.html       # Login page
│   │       ├── 📄 register.html    # Registration
│   │       ├── 📄 predict.html     # Upload page
│   │       ├── 📄 camera_capture.html # Camera page
│   │       ├── 📄 result.html      # Results page
│   │       ├── 📄 diseasetype.html # Disease info
│   │       ├── 📄 find-specialist.html
│   │       ├── 📄 page1.html       # Disease details
│   │       ├── 📄 page2.html
│   │       ├── 📄 page3.html
│   │       ├── 📄 page4.html
│   │       ├── 📄 page5.html
│   │       ├── 📄 page6.html
│   │       ├── 📄 page7.html
│   │       ├── 📄 page8.html
│   │       ├── 📄 page9.html
│   │       └── 📄 page10.html
│   │
│   └── 📁 .venv/                   # Virtual environment
│       ├── 📁 Lib/
│       ├── 📁 Scripts/
│       └── 📄 pyvenv.cfg
│
└── 📁 deployment/                   # Deployment configs
    ├── 📄 Procfile                 # Heroku/Railway
    ├── 📄 render.yaml              # Render.com
    ├── 📄 railway.json             # Railway.app
    ├── 📄 railway.toml
    ├── 📄 nixpacks.toml
    ├── 📄 vercel.json              # Vercel
    ├── 📄 build.sh                 # Build script
    ├── 📄 DEPLOY_NOW.md            # Deployment guide
    └── 📄 RAILWAY_DEPLOYMENT.md
```

---

## 🔐 SECURITY ARCHITECTURE

### Security Layers Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 1: NETWORK SECURITY                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • HTTPS/SSL Encryption (TLS 1.3)                      │ │
│  │  • Firewall Rules                                      │ │
│  │  • DDoS Protection                                     │ │
│  │  • Rate Limiting (100 req/min per IP)                 │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                 LAYER 2: APPLICATION SECURITY                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • CSRF Protection (Django middleware)                 │ │
│  │  • XSS Prevention (Content Security Policy)           │ │
│  │  • SQL Injection Protection (ORM)                     │ │
│  │  • Clickjacking Protection (X-Frame-Options)          │ │
│  │  • CORS Configuration                                 │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                LAYER 3: AUTHENTICATION & AUTHORIZATION       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • Password Hashing (PBKDF2-SHA256)                   │ │
│  │  • Session Management (Secure cookies)                │ │
│  │  • Token-based Auth (JWT optional)                    │ │
│  │  • Role-based Access Control                          │ │
│  │  • Multi-factor Authentication (Future)               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 4: DATA SECURITY                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • Input Validation & Sanitization                    │ │
│  │  • Output Encoding                                    │ │
│  │  • Secure File Upload                                 │ │
│  │  • Data Encryption at Rest                            │ │
│  │  • Database Access Control                            │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  LAYER 5: MONITORING & LOGGING               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • Security Event Logging                             │ │
│  │  • Intrusion Detection                                │ │
│  │  • Audit Trails                                       │ │
│  │  • Error Monitoring                                   │ │
│  │  • Anomaly Detection                                  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 DATABASE SCHEMA DIAGRAM

### MongoDB Collections Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE: hair_scalp_db                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    COLLECTION: users                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  {                                                      │ │
│  │    "_id": ObjectId("..."),                             │ │
│  │    "username": "john_doe",                             │ │
│  │    "email": "john@example.com",                        │ │
│  │    "password_hash": "$pbkdf2-sha256$...",              │ │
│  │    "created_at": ISODate("2024-01-15T10:30:00Z"),     │ │
│  │    "last_login": ISODate("2024-01-20T14:22:00Z"),     │ │
│  │    "is_active": true,                                  │ │
│  │    "profile": {                                        │ │
│  │      "full_name": "John Doe",                          │ │
│  │      "date_of_birth": ISODate("1990-05-15"),          │ │
│  │      "phone": "+1234567890",                           │ │
│  │      "address": "123 Main St, City",                   │ │
│  │      "preferences": {                                  │ │
│  │        "theme": "dark",                                │ │
│  │        "notifications": true                           │ │
│  │      }                                                  │ │
│  │    }                                                    │ │
│  │  }                                                      │ │
│  └────────────────────────────────────────────────────────┘ │
│  Indexes: email (unique), username (unique)                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  COLLECTION: predictions                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  {                                                      │ │
│  │    "_id": ObjectId("..."),                             │ │
│  │    "user_id": ObjectId("..."),                         │ │
│  │    "image_url": "data:image/jpeg;base64,...",          │ │
│  │    "predicted_class": "Alopecia Areata",               │ │
│  │    "confidence": 0.92,                                 │ │
│  │    "all_probabilities": [                              │ │
│  │      {"class": "Alopecia Areata", "prob": 0.92},      │ │
│  │      {"class": "Psoriasis", "prob": 0.05},            │ │
│  │      ...                                               │ │
│  │    ],                                                   │ │
│  │    "stage_info": {                                     │ │
│  │      "stage": "Early",                                 │ │
│  │      "severity": "Mild",                               │ │
│  │      "days_elapsed": 15,                               │ │
│  │      "progression_rate": "Stable",                     │ │
│  │      "clinical_notes": "Small patches observed..."     │ │
│  │    },                                                   │ │
│  │    "timestamp": ISODate("2024-01-20T14:30:00Z"),      │ │
│  │    "metadata": {                                       │ │
│  │      "device": "mobile",                               │ │
│  │      "browser": "Chrome",                              │ │
│  │      "ip_address": "192.168.1.1"                       │ │
│  │    }                                                    │ │
│  │  }                                                      │ │
│  └────────────────────────────────────────────────────────┘ │
│  Indexes: user_id, timestamp (desc), predicted_class        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   COLLECTION: sessions                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  {                                                      │ │
│  │    "_id": ObjectId("..."),                             │ │
│  │    "session_id": "abc123xyz...",                       │ │
│  │    "user_id": ObjectId("..."),                         │ │
│  │    "data": {                                           │ │
│  │      "last_activity": ISODate("2024-01-20T14:30:00"), │ │
│  │      "preferences": {...}                              │ │
│  │    },                                                   │ │
│  │    "created_at": ISODate("2024-01-20T10:00:00Z"),     │ │
│  │    "expires_at": ISODate("2024-01-21T10:00:00Z"),     │ │
│  │    "ip_address": "192.168.1.1",                        │ │
│  │    "user_agent": "Mozilla/5.0..."                      │ │
│  │  }                                                      │ │
│  └────────────────────────────────────────────────────────┘ │
│  Indexes: session_id (unique), expires_at (TTL)             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   COLLECTION: diseases                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  {                                                      │ │
│  │    "_id": ObjectId("..."),                             │ │
│  │    "name": "Alopecia Areata",                          │ │
│  │    "description": "An autoimmune disorder...",         │ │
│  │    "symptoms": [                                       │ │
│  │      "Patchy hair loss",                               │ │
│  │      "Smooth, round bald spots",                       │ │
│  │      "Sudden hair loss"                                │ │
│  │    ],                                                   │ │
│  │    "causes": [                                         │ │
│  │      "Autoimmune response",                            │ │
│  │      "Genetic factors",                                │ │
│  │      "Stress"                                          │ │
│  │    ],                                                   │ │
│  │    "treatments": [                                     │ │
│  │      "Corticosteroid injections",                      │ │
│  │      "Topical immunotherapy",                          │ │
│  │      "Minoxidil"                                       │ │
│  │    ],                                                   │ │
│  │    "prevention": [                                     │ │
│  │      "Stress management",                              │ │
│  │      "Healthy diet",                                   │ │
│  │      "Regular check-ups"                               │ │
│  │    ],                                                   │ │
│  │    "severity_levels": ["Mild", "Moderate", "Severe"], │ │
│  │    "image_url": "/static/images/alopecia.jpg"          │ │
│  │  }                                                      │ │
│  └────────────────────────────────────────────────────────┘ │
│  Indexes: name (unique)                                     │
└─────────────────────────────────────────────────────────────┘
```

---


## 🚀 DEPLOYMENT ARCHITECTURE

### Production Deployment Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS (Global)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Desktop  │  │  Tablet  │  │  Mobile  │  │   PWA    │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS (Port 443)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CDN (Content Delivery Network)              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  • Static Files (CSS, JS, Images)                          │ │
│  │  • Edge Caching (Faster delivery)                          │ │
│  │  • DDoS Protection                                         │ │
│  │  • SSL Termination                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LOAD BALANCER                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  • Distribute Traffic                                       │ │
│  │  • Health Checks                                           │ │
│  │  • SSL/TLS Termination                                     │ │
│  │  • Session Persistence                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  WEB SERVER  │  │  WEB SERVER  │  │  WEB SERVER  │
│   Instance 1 │  │   Instance 2 │  │   Instance 3 │
│              │  │              │  │              │
│  Gunicorn    │  │  Gunicorn    │  │  Gunicorn    │
│  4 Workers   │  │  4 Workers   │  │  4 Workers   │
│              │  │              │  │              │
│  Django App  │  │  Django App  │  │  Django App  │
│  ML Model    │  │  ML Model    │  │  ML Model    │
└──────────────┘  └──────────────┘  └──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE CLUSTER                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    MongoDB Atlas                            │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │   Primary    │  │  Secondary   │  │  Secondary   │    │ │
│  │  │   (Write)    │  │   (Read)     │  │   (Read)     │    │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │ │
│  │         │                  │                  │            │ │
│  │         └──────────────────┴──────────────────┘            │ │
│  │                    Replication                              │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKUP & MONITORING                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  • Automated Backups (Daily)                               │ │
│  │  • Point-in-time Recovery                                  │ │
│  │  • Performance Monitoring                                  │ │
│  │  • Error Tracking (Sentry)                                 │ │
│  │  • Log Aggregation                                         │ │
│  │  • Alerting System                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Deployment Platforms Comparison
```
┌─────────────────────────────────────────────────────────────────┐
│                    RENDER.COM (Current)                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Pros:                                                      │ │
│  │  ✓ Easy deployment (Git push)                              │ │
│  │  ✓ Free tier available                                     │ │
│  │  ✓ Auto-scaling                                            │ │
│  │  ✓ Free SSL certificates                                   │ │
│  │  ✓ Built-in CI/CD                                          │ │
│  │                                                             │ │
│  │  Cons:                                                      │ │
│  │  ✗ Limited free tier resources                             │ │
│  │  ✗ Cold starts on free tier                                │ │
│  │  ✗ Less control than AWS                                   │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       RAILWAY.APP                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Pros:                                                      │ │
│  │  ✓ Simple configuration                                    │ │
│  │  ✓ GitHub integration                                      │ │
│  │  ✓ Database hosting included                               │ │
│  │  ✓ Environment variables management                        │ │
│  │                                                             │ │
│  │  Cons:                                                      │ │
│  │  ✗ Pricing can increase quickly                            │ │
│  │  ✗ Limited free tier                                       │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         HEROKU                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Pros:                                                      │ │
│  │  ✓ Mature platform                                         │ │
│  │  ✓ Extensive add-ons ecosystem                             │ │
│  │  ✓ Great documentation                                     │ │
│  │  ✓ Easy scaling                                            │ │
│  │                                                             │ │
│  │  Cons:                                                      │ │
│  │  ✗ No free tier anymore                                    │ │
│  │  ✗ More expensive than alternatives                        │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    AWS/GCP/AZURE (Enterprise)                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Pros:                                                      │ │
│  │  ✓ Full control and flexibility                            │ │
│  │  ✓ Advanced features                                       │ │
│  │  ✓ Best for large scale                                    │ │
│  │  ✓ Enterprise support                                      │ │
│  │                                                             │ │
│  │  Cons:                                                      │ │
│  │  ✗ Complex setup                                           │ │
│  │  ✗ Requires DevOps expertise                               │ │
│  │  ✗ Can be expensive                                        │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 CI/CD PIPELINE

### Continuous Integration & Deployment Flow
```
┌─────────────────────────────────────────────────────────────────┐
│                    DEVELOPER WORKFLOW                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  1. Write Code                                             │ │
│  │  2. Run Local Tests                                        │ │
│  │  3. Commit to Git                                          │ │
│  │  4. Push to GitHub                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB REPOSITORY                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  • Version Control                                         │ │
│  │  • Branch Management                                       │ │
│  │  • Pull Request Reviews                                    │ │
│  │  • Issue Tracking                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Webhook Trigger
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS (CI)                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Step 1: Checkout Code                                     │ │
│  │  ├─ git clone repository                                   │ │
│  │  └─ checkout branch                                        │ │
│  │                                                             │ │
│  │  Step 2: Setup Environment                                 │ │
│  │  ├─ Install Python 3.11                                    │ │
│  │  ├─ Create virtual environment                             │ │
│  │  └─ Install dependencies                                   │ │
│  │                                                             │ │
│  │  Step 3: Run Tests                                         │ │
│  │  ├─ Unit tests (pytest)                                    │ │
│  │  ├─ Integration tests                                      │ │
│  │  ├─ Code coverage                                          │ │
│  │  └─ Linting (flake8, black)                                │ │
│  │                                                             │ │
│  │  Step 4: Security Scan                                     │ │
│  │  ├─ Dependency vulnerabilities                             │ │
│  │  ├─ Code security issues                                   │ │
│  │  └─ Secret detection                                       │ │
│  │                                                             │ │
│  │  Step 5: Build Application                                 │ │
│  │  ├─ Collect static files                                   │ │
│  │  ├─ Run migrations (dry-run)                               │ │
│  │  └─ Create build artifacts                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Tests Pass?
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT (CD)                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Step 1: Deploy to Staging                                 │ │
│  │  ├─ Deploy to staging environment                          │ │
│  │  ├─ Run smoke tests                                        │ │
│  │  └─ Manual approval (optional)                             │ │
│  │                                                             │ │
│  │  Step 2: Deploy to Production                              │ │
│  │  ├─ Blue-green deployment                                  │ │
│  │  ├─ Health checks                                          │ │
│  │  ├─ Gradual rollout                                        │ │
│  │  └─ Monitor metrics                                        │ │
│  │                                                             │ │
│  │  Step 3: Post-Deployment                                   │ │
│  │  ├─ Run database migrations                                │ │
│  │  ├─ Clear caches                                           │ │
│  │  ├─ Verify deployment                                      │ │
│  │  └─ Send notifications                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING & ALERTS                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  • Application Performance Monitoring                      │ │
│  │  • Error Tracking                                          │ │
│  │  • Log Aggregation                                         │ │
│  │  • Uptime Monitoring                                       │ │
│  │  • Alert Notifications (Email, Slack)                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📱 MOBILE & PWA ARCHITECTURE

### Progressive Web App Structure
```
┌─────────────────────────────────────────────────────────────────┐
│                    PWA COMPONENTS                                │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Web App Manifest                          │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  {                                                    │  │ │
│  │  │    "name": "Hair & Scalp AI",                        │  │ │
│  │  │    "short_name": "Scalp AI",                         │  │ │
│  │  │    "start_url": "/",                                 │  │ │
│  │  │    "display": "standalone",                          │  │ │
│  │  │    "background_color": "#0f172a",                    │  │ │
│  │  │    "theme_color": "#14b8a6",                         │  │ │
│  │  │    "icons": [...]                                    │  │ │
│  │  │  }                                                    │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Service Worker                            │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  • Offline Support                                   │  │ │
│  │  │  • Cache Management                                  │  │ │
│  │  │  • Background Sync                                   │  │ │
│  │  │  • Push Notifications                                │  │ │
│  │  │  • Update Management                                 │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Cache Strategy                            │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Cache First:                                        │  │ │
│  │  │  • Static assets (CSS, JS, images)                  │  │ │
│  │  │  • App shell                                         │  │ │
│  │  │                                                       │  │ │
│  │  │  Network First:                                      │  │ │
│  │  │  • API calls                                         │  │ │
│  │  │  • Dynamic content                                   │  │ │
│  │  │                                                       │  │ │
│  │  │  Stale While Revalidate:                             │  │ │
│  │  │  • User data                                         │  │ │
│  │  │  • Predictions history                               │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Install Prompt                            │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  • Detect install capability                         │  │ │
│  │  │  • Show custom install UI                            │  │ │
│  │  │  • Handle install event                              │  │ │
│  │  │  • Track installation                                │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 PERFORMANCE OPTIMIZATION

### Optimization Layers
```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND OPTIMIZATION                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  • Minify CSS/JS (reduce file size by 60%)                │ │
│  │  • Image Compression (WebP format, lazy loading)          │ │
│  │  • Code Splitting (load only what's needed)               │ │
│  │  • Browser Caching (Cache-Control headers)                │ │
│  │  • CDN for Static Files (faster delivery)                 │ │
│  │  • Preload Critical Resources                             │ │
│  │  • Defer Non-Critical JavaScript                          │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND OPTIMIZATION                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  • Database Indexing (faster queries)                      │ │
│  │  • Query Optimization (reduce DB calls)                    │ │
│  │  • Connection Pooling (reuse connections)                  │ │
│  │  • Caching Layer (Redis for frequent data)                │ │
│  │  • Async Tasks (Celery for background jobs)               │ │
│  │  • Gzip Compression (reduce response size)                │ │
│  │  • API Response Pagination                                │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    ML MODEL OPTIMIZATION                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  • Model Quantization (reduce model size)                  │ │
│  │  • Batch Inference (process multiple images)              │ │
│  │  • Model Caching (keep model in memory)                   │ │
│  │  • GPU Acceleration (if available)                        │ │
│  │  • ONNX Runtime (faster inference)                        │ │
│  │  • TensorRT Optimization                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE OPTIMIZATION                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  • Load Balancing (distribute traffic)                     │ │
│  │  • Auto-Scaling (handle traffic spikes)                    │ │
│  │  • Database Replication (read replicas)                    │ │
│  │  • CDN Integration (global content delivery)              │ │
│  │  • HTTP/2 Support (multiplexing)                           │ │
│  │  • Keep-Alive Connections                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

**End of Domain Architecture Documentation**

*Complete technical reference for Hair & Scalp Disease Prediction System*
*Version 1.0 - Comprehensive Architecture Guide*

