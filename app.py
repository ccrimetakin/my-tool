import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter
import io
import requests

# Page Config
st.set_page_config(page_title="AI Photo Studio Max", layout="wide")

# Advanced CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(45deg, #FF4B2B, #FF416C); color: white; border: none; border-radius: 5px; height: 50px; font-weight: bold; width: 100%; }
    .stSidebar { background-color: #161b22; }
    div[data-testid="stExpander"] { background: #1f2937; border-radius: 10px; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ AI Photo Studio Max")
st.write("Advance AI tools se apni photo ko modify karein.")

# --- Sidebar: Tools & Filters ---
st.sidebar.header("🛠️ Editor Tools")

# 1. Background Logic
bg_mode = st.sidebar.selectbox("Background Mode:", ["Transparent", "Solid Color", "Stock Image", "AI Generated (Coming Soon)"])

bg_color = "#ffffff"
if bg_mode == "Solid Color":
    bg_color = st.sidebar.color_picker("Pick a Color", "#0000FF")
elif bg_mode == "Stock Image":
    stock = st.sidebar.selectbox("Select Theme:", ["Luxury Office", "Cyberpunk City", "Nature", "Studio Minimal"])
    # Links setup yahan honge...

# 2. Color Effects (Brightness, Contrast, etc.)
st.sidebar.subheader("🎨 Color Effects")
brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
saturation = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0)
blur = st.sidebar.slider("Blur Effect", 0, 10, 0)

# 3. Photo Filters
filter_type = st.sidebar.selectbox("Apply Filter:", ["None", "Black & White", "Sepia", "Vivid", "Soft Glow"])

# --- Main App ---
upload = st.file_uploader("Apni Photo Upload Karein", type=["jpg", "png", "jpeg"])

if upload:
    col1, col2 = st.columns(2)
    input_img = Image.open(upload)
    
    with col1:
        st.image(input_img, caption="Original Photo", use_container_width=True)

    if st.button("Apply Magic ✨"):
        with st.spinner("AI processing chal rahi hai..."):
            # A. Remove Background
            img_bytes = upload.getvalue()
            res_bytes = remove(img_bytes)
            subject = Image.open(io.BytesIO(res_bytes)).convert("RGBA")

            # B. Apply Color Enhancements
            enhancer = ImageEnhance.Brightness(subject)
            subject = enhancer.enhance(brightness)
            enhancer = ImageEnhance.Contrast(subject)
            subject = enhancer.enhance(contrast)
            enhancer = ImageEnhance.Color(subject)
            subject = enhancer.enhance(saturation)
            
            if blur > 0:
                subject = subject.filter(ImageFilter.GaussianBlur(blur))

            # C. Apply Background Mode
            if bg_mode == "Solid Color":
                h = bg_color.lstrip('#')
                rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                new_bg = Image.new("RGBA", subject.size, rgb + (255,))
                final_img = Image.alpha_composite(new_bg, subject)
            else:
                final_img = subject # Simplification for demo

            # D. Apply Filters
            if filter_type == "Black & White":
                final_img = final_img.convert("L")
            elif filter_type == "Sepia":
                # Sepia logic...
                pass

            with col2:
                st.image(final_img, caption="AI Result", use_container_width=True)
                
            # Download
            buf = io.BytesIO()
            final_img.convert("RGB").save(buf, format="JPEG")
            st.download_button("📥 Download Result", buf.getvalue(), "ai_photo.jpg", "image/jpeg")

st.info("💡 Tip: AI Generated Background feature ke liye hum DALL-E ya Stable Diffusion API integrate kar sakte hain.")
