# 🫁 Pneumonia Detection - AI Medical Imaging Application

A full-stack web application that uses deep learning to detect pneumonia in chest X-ray images. Built with FastAPI backend and modern React frontend.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![React](https://img.shields.io/badge/react-19-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.100%2B-green)

## 🌟 Features

### Backend
- **FastAPI REST API** for fast, production-ready inference
- **Deep Learning Model** (ResNet50) trained on chest X-ray dataset
- **Real-time Predictions** with confidence scores
- **CORS Support** for frontend integration
- **Comprehensive Error Handling** and validation
- **Model Health Checks** and diagnostics
- **API Documentation** with Swagger UI

### Frontend
- **Intuitive UI** for uploading and analyzing X-ray images
- **Drag & Drop Support** for easy image uploads
- **Real-time Preview** of uploaded images
- **Animated Results Display** with confidence visualization
- **Responsive Design** (mobile, tablet, desktop)
- **Error Handling** with user-friendly messages
- **Fast Performance** with Vite build tool
- **Modern React** with hooks and best practices

## 📋 Project Structure

```
pneumonia_detection/
├── app.py                      # Legacy Flask application
├── chest_xray_model.h5         # Trained model file
├── pneumonia_detection.ipynb   # Model training notebook
├── SETUP.md                    # Detailed setup guide
├── README.md                   # This file
├── backend/
│   ├── fastapi_app.py          # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Backend documentation
└── frontend/
    ├── package.json            # npm dependencies
    ├── src/
    │   ├── App.jsx             # Main React component
    │   ├── App.css             # Styles
    │   └── main.jsx            # Entry point
    └── README.md               # Frontend documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- Trained model file: `chest_xray_model.h5`

### Backend Setup (5 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Prepare model
mkdir -p model
cp ../chest_xray_model.h5 model/pneumonia_resnet50.h5

# Run server
python -m uvicorn fastapi_app:app --reload
```

Server runs at: `http://localhost:8000`

### Frontend Setup (5 minutes)

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Start dev server
npm run dev
```

App runs at: `http://localhost:5173`

## 🎯 Usage

1. **Open the Application**: Navigate to `http://localhost:5173`
2. **Upload X-Ray**: Drag and drop a chest X-ray image (JPEG/PNG, max 10MB)
3. **Analyze**: Click "Analyze Image" button
4. **View Results**: See diagnosis and confidence percentage
5. **Repeat**: Analyze more images as needed

## 📊 API Documentation

### Health Check
```bash
GET /health
```

Response:
```json
{"status": "ok", "model_loaded": true}
```

### Predict Pneumonia
```bash
POST /predict
Content-Type: multipart/form-data

file: <image_file>
```

Response:
```json
{
  "label": "Pneumonia",
  "confidence": 95.23,
  "raw_score": 0.9523
}
```

Interactive API docs: `http://localhost:8000/docs`

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern web framework
- **TensorFlow/Keras** - Deep learning
- **Python** - Backend language
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Frontend
- **React 19** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **CSS3** - Styling with animations
- **JavaScript ES6+** - Programming language

## 📱 Device Support

- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Tablet (iOS, Android)
- ✅ Mobile phones
- ✅ All modern browsers

## 🔧 Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn fastapi_app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
# Output in dist/
```

**Backend:**
Deploy `fastapi_app.py` to your hosting platform (Heroku, AWS, Google Cloud, etc.)

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Comprehensive setup guide
- **[backend/README.md](backend/README.md)** - Backend documentation
- **[frontend/README.md](frontend/README.md)** - Frontend documentation

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application is for **educational and research purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.

**Always consult a qualified radiologist or healthcare professional for:**
- Accurate diagnosis
- Treatment decisions
- Medical advice

This tool should only be used as a supplementary aid in educational settings or research environments.

## 🧠 Model Information

- **Architecture**: ResNet50
- **Input Size**: 224x224 pixels
- **Preprocessing**: Normalization (1/255)
- **Output**: Binary classification (Pneumonia/Normal)
- **Framework**: TensorFlow/Keras

## 📈 Performance

- **Inference Time**: < 500ms per image
- **Accuracy**: [See model training notebook]
- **File Size**: ~100MB (model)
- **Frontend Bundle**: ~50KB (gzipped)

## 🐛 Troubleshooting

### Backend Issues
```bash
# Port already in use
lsof -i :8000  # Find process
kill -9 <PID>  # Kill process

# Model not found
mkdir -p backend/model
cp chest_xray_model.h5 backend/model/pneumonia_resnet50.h5

# Dependencies issue
pip install --upgrade -r requirements.txt
```

### Frontend Issues
```bash
# Build fails
rm -rf node_modules
npm install
npm run build

# Port conflicts
npm run dev -- --port 5174
```

See **[SETUP.md](SETUP.md)** for more troubleshooting.

## 🚀 Deployment

### Frontend (Vercel)
1. Push code to GitHub
2. Import project on Vercel
3. Set `VITE_API_URL` to production backend
4. Deploy!

### Backend (Heroku)
1. Create Heroku app
2. Push code to Heroku
3. Set config vars
4. Deploy!

See **[SETUP.md](SETUP.md)** for detailed deployment instructions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as an educational project for medical AI learning.

## 📞 Support

- Check [SETUP.md](SETUP.md) for setup help
- Review API docs at `http://localhost:8000/docs`
- Check backend and frontend READMEs for component-specific help
- Review project notebook for model training details

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **TensorFlow**: https://www.tensorflow.org/
- **Medical AI**: https://cs231n.stanford.edu/

---

**Disclaimer**: This project is for educational purposes. Do not use for actual medical diagnosis without professional oversight.
