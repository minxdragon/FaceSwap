#! /usr/bin/env python
import os
import cv2
import numpy
import argparse
import streamlit as st
import replicate
import numpy as np
from  PIL import Image, ImageEnhance
import requests
from io import BytesIO

from urllib.request import urlopen, Request
from face_detection import select_face, select_all_faces
from face_swap import face_swap

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FaceSwapApp')
    parser.add_argument('--correct_color', default=True, action='store_true', help='Correct color')
    parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
    args = parser.parse_args()
    
    uploaded_target_file = st.camera_input("Take a picture")
    prompt = st.text_input('Prompt ')

    if uploaded_target_file is not None:
        # To read image file buffer as a PIL Image:
        img = Image.open(uploaded_target_file)

        # To convert PIL Image to numpy array:
        img_array = np.array(img)

        # Check the type of img_array:
        # Should output: <class 'numpy.ndarray'>
        st.write(type(img_array))

        # Check the shape of img_array:
        # Should output shape: (height, width, channels)
        st.write(img_array.shape)

    model = replicate.models.get("stability-ai/stable-diffusion")
    init_image = uploaded_target_file
    print (init_image)
    
    output_url = model.predict(prompt=(prompt), init_image=(init_image))[0]
    print(output_url)
        # download the image, convert it to a NumPy array, and then read
    response = requests.get(output_url)
    img = Image.open(BytesIO(response.content))
    #uploaded_source_file = st.file_uploader("Upload a source image", type=["png", "jpg", "jpeg"])

    if uploaded_target_file is not None and img is not None and prompt is not None:

        # stable diffusion script
        model = replicate.models.get("stability-ai/stable-diffusion")
        init_image = uploaded_target_file #not currently working
        print (init_image)
        output_url = model.predict(prompt=(prompt), init_image=(init_image))[0]
        print(output_url)
        # download the image, convert it to a NumPy array, and then read
        response = requests.get(output_url)
        img = Image.open(BytesIO(response.content))

        source_image = img
        target_image = Image.open(uploaded_target_file)
    
       # Convert images from PIL to CV2
        src_img = cv2.cvtColor(numpy.array(source_image), cv2.IMREAD_COLOR)
        dst_img = cv2.cvtColor(numpy.array(target_image), cv2.IMREAD_COLOR)
    

       # Select src face
        src_points, src_shape, src_face = select_face(src_img)
       # Select dst face
        dst_faceBoxes = select_all_faces(dst_img)

        if dst_faceBoxes is None:
          print('Detect 0 Face !!!')
          exit(-1)

        output = dst_img
        for k, dst_face in dst_faceBoxes.items():
           output = face_swap(src_face, dst_face["face"], src_points,
                           dst_face["points"], dst_face["shape"],
                           output, args)

           st.markdown('<p style="text-align: left;">Result</p>',unsafe_allow_html=True)
           st.image(output,width=500)       