import cv2
import pytesseract
from pyzbar.pyzbar import decode
import re
import numpy as np
from PIL import Image
import io
import base64

class CardScanner:
    @staticmethod
    def decode_image(base64_image):
        # Convert base64 to image
        image_data = base64.b64decode(base64_image.split(',')[1])
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Process image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(binary)
        
        # Extract card details using regex
        card_number = re.search(r'4198\d{12}', text)
        account_number = re.search(r'01S\d{8}', text)
        name = re.search(r'[A-Z]+\s+[A-Z]+(?:\s+[A-Z]+)?', text)
        
        return {
            'card_number': card_number.group() if card_number else None,
            'account_number': account_number.group() if account_number else None,
            'customer_name': name.group() if name else None
        }

def process_signature_to_png(base64_image):
    """Convert signature to PNG with transparent background"""
    try:
        # Decode base64 image
        format_type, imgstr = base64_image.split(';base64,')
        image_data = base64.b64decode(imgstr)
        
        # Convert to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 11, 2)
        
        # Clean up image
        kernel = np.ones((2,2), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Create RGBA image
        rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        
        # Set white pixels to transparent
        rgba[thresh == 0] = [0, 0, 0, 0]
        
        # Convert to PIL Image
        img_pil = Image.fromarray(cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA))
        
        # Save with transparency
        img_byte_arr = io.BytesIO()
        img_pil.save(img_byte_arr, format='PNG', optimize=False, quality=100)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Convert back to base64
        img_str = base64.b64encode(img_byte_arr).decode('utf-8')
        return f'data:image/png;base64,{img_str}'
        
    except Exception as e:
        print(f"Error processing signature: {str(e)}")
        return base64_image