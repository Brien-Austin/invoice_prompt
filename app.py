from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API"))

#function to load genai
model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded):
    if uploaded is not None:
        bytes_data = uploaded.getvalue()
        
        image_parts = [
            {
                "mime_type":uploaded.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not uploaded")

#streamlit
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")
input = st.text_input("Input Prompt",key="input")
uploaded = st.file_uploader("Choose an image...",type=["jpg","jpeg","png","pdf"])
image=""
if uploaded is not None:
    image=Image.open(uploaded)
    st.image(image,caption="Uploaded image ... ",use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """You are an expert in understanding invoices. We will upload a image as invoice and you will have to answer my questions based on uploaded invoice image"""
if submit:
    image_data= input_image_details(uploaded)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is:")
    st.write(response)