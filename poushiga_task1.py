# -*- coding: utf-8 -*-
"""poushiga_task1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yWqf_uLxdN0PQgmiPIkO8OyQwc_wGe0Z

The task is to extract key-value pairs from the document (image document) where the ticked checkboxes of the form have to be captured properly.

You can use any of the computer vision techniques to make it capture the ticked box values or use any LLM such as GPT Image Vision or a combination of both.

But the output should be an accurate JSON representation of the image, able to capture all the information accurately, especially the ticked checkbox values

Steps
1. Preprocessing the Image:
Use OpenCV or a similar library to preprocess the image.
Convert the image to grayscale.
Apply image binarization (like Otsu's thresholding) to enhance the checkboxes and text.
Use edge detection (Canny Edge Detection) to help identify form boundaries and checkbox outlines.
2. Identifying Checkboxes:
Detect the checkboxes using contour detection with OpenCV.
You can use shape detection algorithms to find rectangular regions (checkboxes).
Crop each checkbox region and check if it’s filled or not using color intensity, or perform template matching to detect ticks in the checkboxes.
3. Text Extraction:
Apply Tesseract OCR or another OCR tool to extract the form text, especially the key-value pairs.
Post-process the extracted text to remove noise and structure it based on form layout.
4. Combining with GPT-4 Vision:
Use GPT-4 with Vision capabilities to help in interpreting and verifying OCR results.
Specifically, use GPT-4 to cross-verify checkbox detection (from computer vision) and interpret any unclear texts or symbols.
5. JSON Structuring:
Organize the extracted data into key-value pairs.
Structure the output into a JSON format, where keys are the form labels and values include both the filled text and the ticked or unticked checkboxes.
Python Implementation Strategy
Libraries Needed:
opencv-python: For image preprocessing and checkbox detection.
pytesseract: For OCR.
PIL (Pillow): For handling image processing.
transformers: For GPT-4 Vision (if integrating with an API).
"""



import cv2
import pytesseract
import json
from PIL import Image

# Step 1: Preprocess the image using OpenCV
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return binary_img

# Step 2: Detect checkboxes and check if they are ticked
def detect_checkboxes(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    checkbox_status = {}

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:  # assuming checkboxes are square/rectangular
            x, y, w, h = cv2.boundingRect(contour)
            checkbox_roi = image[y:y+h, x:x+w]

            # Check if the checkbox is ticked (analyzing pixel density)
            if cv2.countNonZero(checkbox_roi) > (w * h * 0.2):  # Arbitrary threshold for "tick"
                checkbox_status[(x, y)] = "ticked"
            else:
                checkbox_status[(x, y)] = "unticked"

    return checkbox_status

# Step 3: Extract text from the document
def extract_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

# Step 4: Combine the text and checkboxes into JSON
def create_json_structure(text, checkboxes):
    # Parse the text into key-value pairs based on form layout
    # You might need to custom-parse depending on the form structure.
    key_value_pairs = {}

    # Example: simple parsing (would need adjustment for real forms)
    lines = text.split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            key_value_pairs[key.strip()] = value.strip()

    # Add checkbox information
    key_value_pairs['checkboxes'] = checkboxes

    return json.dumps(key_value_pairs, indent=4)

# Putting it all together
image_path = 'path_to_form_image.jpeg'
preprocessed_image = preprocess_image(image_path)
checkboxes = detect_checkboxes(preprocessed_image)
extracted_text = extract_text(image_path)

# Create the final JSON structure
form_json = create_json_structure(extracted_text, checkboxes)
print(form_json)