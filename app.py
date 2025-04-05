import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

MODAL_URL = "https://trish404--style-lora-backend.modal.run/run_backend"

def call_modal(prompt, style):
    response = requests.post(MODAL_URL, json={"prompt": prompt, "style": style})
    data = response.json()

    if "error" in data:
        return None, data["error"], ""
    
    image_data = base64.b64decode(data["image"])
    image = Image.open(BytesIO(image_data))
    return image, data["caption"], data["enhanced"]

st.title("🎨 AI Image Generator with Style LoRA")

user_prompt = st.text_input("Enter a prompt:")
style = st.selectbox("Choose style", ["none", "cyberpunk", "anime"])

if st.button("Generate"):
    with st.spinner("Generating image..."):
        image, caption, enhanced = call_modal(user_prompt, style)

    if image:
        st.image(image, caption=caption, use_column_width=True)
        st.caption(f"✨ Enhanced Prompt: {enhanced}")
    else:
        st.error(caption)
