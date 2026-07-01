# Pneumonia Detection Application - Setup Guide

Complete setup instructions for running the Pneumonia Detection application with both frontend and backend.

## Project Structure

```
pneumonia_detection/
├── app.py                      # Legacy standalone Flask app
├── chest_xray_model.h5         # Trained model file
├── pneumonia_detection.ipynb   # Jupyter notebook with model training
├── run.bat                     # Windows batch script to run both servers
├── backend/
│   ├── fastapi_app.py          # FastAPI backend application
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Backend documentation
├── frontend/
│   ├── package.json            # npm dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── .env.example            # Example environment variables
│   ├── index.html              # HTML template
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css             # Application styles
│   │   ├── main.jsx            # React entry point
│   │   └── index.css           # Global styles
│   ├── public/                 # Static assets
│   └── README.md               # Frontend documentation
```

## Prerequisites

### For Backend
- Python 3.8+ (recommended 3.10 or 3.11)
- pip (Python package manager)
- TensorFlow/Keras model file: `chest_xray_model.h5` or `pneumonia_resnet50.h5`

### For Frontend
- Node.js 16+
- npm 8+ or yarn

## Backend Setup

### 1. Install Python Dependencies

Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Prepare the Model

The FastAPI app expects the model at `backend/model/pneumonia_resnet50.h5`. You have two options:

**Option A: Copy existing model**
```bash
# From project root
mkdir -p backend/model
cp chest_xray_model.h5 backend/model/pneumonia_resnet50.h5
```

**Option B: Train the model**
```bash
# Run the Jupyter notebook to train the model
jupyter notebook pneumonia_detection.ipynb
```

### 3. Run Backend Server

From the `backend` directory:
```bash
python -m uvicorn fastapi_app:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Frontend Setup

### 1. Install Dependencies

Navigate to the frontend directory:
```bash
cd frontend
```

Install npm packages:
```bash
npm install
```

### 2. Configure Environment

Create `.env.local` from `.env.example`:
```bash
cp .env.example .env.local
```

Edit `.env.local` if backend runs on a different URL:
```
VITE_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Running Both Servers

### Option 1: Separate Terminals

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
# Activate venv (see instructions above)
pip install -r requirements.txt
python -m uvicorn fastapi_app:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Option 2: Using run.bat (Windows Only)

If using Windows, you can use the provided `run.bat` script:
```bash
run.bat
```

This will start both servers in separate windows.

### Option 3: Production Build

Build the frontend:
```bash
cd frontend
npm run build
```

This creates a `dist` directory with optimized production files.

## Accessing the Application

1. **Frontend**: Open browser to `http://localhost:5173`
2. **Backend API**: `http://localhost:8000`
3. **API Docs**: `http://localhost:8000/docs` (Swagger UI)
4. **ReDoc Docs**: `http://localhost:8000/redoc`

## Testing the Application

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok", "model_loaded": true}
```

### 2. Upload and Predict

Using the frontend UI:
1. Navigate to `http://localhost:5173`
2. Drag and drop a chest X-ray image
3. Click "Analyze Image"
4. View results with confidence score

Using curl (backend only):
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@path/to/image.jpg"
```

## Deployment

### Frontend Deployment (Vercel/Netlify)

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Deploy the `dist` folder to Vercel or Netlify

3. Set environment variable `VITE_API_URL` to your production backend URL

### Backend Deployment (Heroku/AWS/Google Cloud)

1. Update model path in `fastapi_app.py` if needed
2. Deploy to your chosen platform
3. Ensure CORS is properly configured

## Troubleshooting

### Backend Won't Start

```bash
# Check Python version
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check if port 8000 is available
netstat -tuln | grep 8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows
```

### Frontend Build Fails

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf dist .vite
npm run build
```

### Model Not Loading

1. Verify model file exists at `backend/model/pneumonia_resnet50.h5`
2. Check model file is valid (not corrupted)
3. Check backend logs for specific error
4. Try training a new model with the Jupyter notebook

### API Connection Issues

1. Verify backend is running on port 8000
2. Check `VITE_API_URL` in frontend `.env.local`
3. Verify CORS is enabled in backend
4. Check browser console for specific errors

### Port Already in Use

```bash
# Find process using port 8000 or 5173
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process (get PID from above and run)
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

## Project Features

### Backend
- FastAPI REST API
- Deep Learning inference with TensorFlow
- CORS support for frontend
- Comprehensive error handling
- Model health checks
- Request validation

### Frontend
- Modern React UI
- Drag-and-drop file upload
- Real-time image preview
- Animated results display
- Confidence visualization
- Responsive design
- Error handling and validation

## Medical Disclaimer

⚠️ **IMPORTANT**: This application is for **educational and research purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified radiologist or healthcare professional for accurate diagnosis and treatment decisions.

## Next Steps

1. Explore the API documentation at `http://localhost:8000/docs`
2. Test the frontend with sample X-ray images
3. Review backend code in [backend/README.md](backend/README.md)
4. Review frontend code in [frontend/README.md](frontend/README.md)
5. Configure for production deployment

## Support

For detailed setup information:
- Backend: See [backend/README.md](backend/README.md)
- Frontend: See [frontend/README.md](frontend/README.md)

## License

This project is open source. See individual component READMEs for license information.
