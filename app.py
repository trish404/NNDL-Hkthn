import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

MODAL_URL = "https://trish404--style-lora-backend.modal.run/run_backend"

def call_modal(prompt, style):
    try:
        response = requests.post(MODAL_URL, json={"prompt": prompt, "style": style})
        print("Status Code:", response.status_code)
        print("Raw Text:", response.text)  # This will appear in Streamlit Cloud logs
        data = response.json()
        return Image.open(BytesIO(base64.b64decode(data["image"]))), data["caption"], data["enhanced"]
    except Exception as e:
        return None, f"❌ Error from backend: {str(e)}", ""


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
