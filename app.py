import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance
import io
import requests
import urllib.parse

# Page UI Config
st.set_page_config(page_title="AI Photo Studio Max", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background: linear-gradient(45deg, #00dbde 0%, #fc00ff 100%); color: white; border: none; font-weight: bold; width: 100%; border-radius: 10px; }
    .stDownloadButton>button { background-color: #28a745; color: white; width: 100%; border-radius: 10px; }
    div[data-testid="stSidebar"] { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AI Photo Studio Max (Free Edition)")
st.write("AI se background hatayein aur naya **AI Background** generate karein!")

# --- Sidebar ---
st.sidebar.header("🎨 Design Tools")
mode = st.sidebar.selectbox("Background Type:", ["Transparent", "Solid Color", "AI Magic Generate"])

bg_color = "#ffffff"
ai_prompt = ""

if mode == "Solid Color":
    bg_color = st.sidebar.color_picker("Rang Chunein", "#007BFF")
elif mode == "AI Magic Generate":
    ai_prompt = st.sidebar.text_area("Kaisa background chahiye? (English mein likhein)", "Luxury office interior, cinematic lighting, 8k")
    st.sidebar.info("Tip: 'Nature', 'Cyberpunk City', ya 'Modern Studio' try karein.")

# Color Adjustments
st.sidebar.subheader("✨ Adjustments")
bright = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
cont = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)

# --- Main Section ---
upload = st.file_uploader("Apni Photo Upload karein", type=["jpg", "png", "jpeg"])

if upload:
    c1, c2 = st.columns(2)
    input_img = Image.open(upload)
    
    with c1:
        st.image(input_img, caption="Original Photo", use_container_width=True)

    if st.button("Generate Magic Photo ✨"):
        with st.spinner("AI Background Generate ho raha hai... (Isme 5-10 sec lag sakte hain)"):
            
            # 1. Subject (Person) ka background hatana
            img_bytes = upload.getvalue()
            subject_bytes = remove(img_bytes)
            subject = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")

            # 2. Enhancements
            subject = ImageEnhance.Brightness(subject).enhance(bright)
            subject = ImageEnhance.Contrast(subject).enhance(cont)

            # 3. Background Setup
            if mode == "Transparent":
                final_img = subject
            elif mode == "Solid Color":
                h = bg_color.lstrip('#')
                rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                new_bg = Image.new("RGBA", subject.size, rgb + (255,))
                final_img = Image.alpha_composite(new_bg, subject)
            elif mode == "AI Magic Generate":
                # AI Image Generation using Pollinations (HuggingFace based)
                encoded_prompt = urllib.parse.quote(ai_prompt)
                seed = 42 # Random seed for variety
                gen_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={subject.width}&height={subject.height}&seed={seed}&nologo=true"
                
                try:
                    response = requests.get(gen_url)
                    bg_gen = Image.open(io.BytesIO(response.content)).convert("RGBA")
                    # Resize generated background to match photo
                    bg_gen = bg_gen.resize(subject.size, Image.Resampling.LANCZOS)
                    final_img = Image.alpha_composite(bg_gen, subject)
                except:
                    st.error("AI Background generate nahi ho paya. Internet check karein.")
                    final_img = subject

            with c2:
                st.image(final_img, caption="AI Generated Result", use_container_width=True)
            
            # 4. Download
            buf = io.BytesIO()
            if mode == "Transparent":
                final_img.save(buf, format="PNG")
                btn_label = "📥 Download PNG"
                m_type = "image/png"
            else:
                final_img.convert("RGB").save(buf, format="JPEG")
                btn_label = "📥 Download JPG"
                m_type = "image/jpeg"
                
            st.download_button(btn_label, buf.getvalue(), "ai_studio_photo.jpg", m_type)

st.divider()
st.write("© 2025 AI Studio Max | Powered by HuggingFace & Pollinations")
