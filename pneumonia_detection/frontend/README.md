# Pneumonia Detection Frontend

A modern React web application for pneumonia detection using chest X-ray images. This frontend communicates with a FastAPI backend that runs a deep learning model for medical image classification.

## Features

- 🖼️ **Image Upload**: Drag & drop or click to upload chest X-ray images
- 🤖 **AI Analysis**: Real-time pneumonia detection using ResNet50 deep learning model
- 📊 **Confidence Score**: Visual confidence percentage with animated progress bar
- 🎨 **Responsive Design**: Beautiful, modern UI that works on all devices
- ⚠️ **Health Warnings**: Clear disclaimers for medical use
- ♿ **Accessible**: WCAG compliant interface
- ⚡ **Fast**: Built with Vite for optimal performance

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running (see backend README)

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file based on `.env.example`:
```bash
cp .env.example .env.local
```

4. Update `VITE_API_URL` in `.env.local` if your backend is running on a different URL:
```
VITE_API_URL=http://localhost:8000
```

## Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173` (Vite default port)

## Build

Create an optimized production build:
```bash
npm run build
```

Output files will be in the `dist/` directory.

## Preview Production Build

Preview the production build locally:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── App.jsx         # Main application component
│   ├── App.css         # Application styles
│   ├── main.jsx        # React entry point
│   └── index.css       # Global styles
├── package.json        # Dependencies and scripts
├── vite.config.js      # Vite configuration
└── index.html          # HTML template
```

## Usage

1. **Upload Image**: Drag a chest X-ray image onto the dropzone or click to browse
2. **Wait for Analysis**: The app will send the image to the backend for analysis
3. **View Results**: See the diagnosis (Pneumonia or Normal) with confidence percentage
4. **Analyze More**: Click "Analyze Another Image" to test another X-ray

## API Integration

The frontend communicates with the backend `/predict` endpoint:

- **URL**: `POST /predict`
- **Request**: Multipart form data with image file
- **Response**:
  ```json
  {
    "label": "Pneumonia" or "Normal",
    "confidence": 95.23,
    "raw_score": 0.9523
  }
  ```

## Configuration

### Environment Variables

- `VITE_API_URL`: Backend API base URL (default: `http://localhost:8000`)

## Deployment

### Deploying to Vercel

1. Push your code to GitHub
2. Import the project on Vercel (select the `frontend` directory)
3. Set environment variables:
   - `VITE_API_URL`: Your production backend URL
4. Deploy!

### Deploying to Netlify

1. Connect your GitHub repository
2. Set the build command: `npm run build`
3. Set the publish directory: `dist`
4. Add environment variables in Netlify dashboard
5. Deploy!

## Technologies Used

- **React 19**: UI framework
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **CSS3**: Modern styling with gradients and animations

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Medical Disclaimer

⚠️ **IMPORTANT**: This tool is for **educational and research purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified radiologist or healthcare professional for accurate diagnosis and treatment decisions.

## Performance Optimization

- Lazy loading of images
- Optimized bundle size with Vite
- CSS animations for smooth UX
- Efficient state management

## Troubleshooting

### API Connection Issues

1. Ensure backend is running: `python -m uvicorn backend.fastapi_app:app --reload`
2. Check `VITE_API_URL` in `.env.local`
3. Verify CORS settings in backend
4. Check browser console for detailed errors

### Image Upload Issues

- Supported formats: JPEG, PNG
- Maximum file size: 10MB
- Ensure image is not corrupted

### Build Issues

```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install

# Clear Vite cache
rm -rf dist .vite
npm run build
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check the backend README and ensure both services are properly configured.
