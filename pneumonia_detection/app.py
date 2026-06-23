import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('chest_xray_model.h5')
    return model

model = load_model()

# Page config
st.set_page_config(page_title="Chest X-Ray Classifier", page_icon="🫁")

st.title("🫁 Chest X-Ray Pneumonia Classifier")
st.write("Upload a chest X-ray image to check for signs of pneumonia.")

# File uploader
uploaded_file = st.file_uploader("Choose an X-ray image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="Uploaded X-Ray", use_column_width=True)

    # Preprocess
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # shape (1, 224, 224, 3)

    # Predict
    with st.spinner("Analyzing..."):
        prediction = model.predict(img_array)[0][0]

    # Result
    st.subheader("Result")
    if prediction > 0.5:
        confidence = prediction * 100
        st.error(f"🔴 PNEUMONIA detected — {confidence:.1f}% confidence")
    else:
        confidence = (1 - prediction) * 100
        st.success(f"🟢 NORMAL — {confidence:.1f}% confidence")

    # Confidence bar
    st.subheader("Confidence Score")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Normal", f"{(1-prediction)*100:.1f}%")
    with col2:
        st.metric("Pneumonia", f"{prediction*100:.1f}%")

    st.progress(float(prediction))

    # Disclaimer
    st.warning("⚠️ This is an AI tool for educational purposes only. Not a substitute for professional medical diagnosis.")