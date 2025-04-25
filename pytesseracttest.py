import pytesseract
from pdf2image import convert_from_path
import os

print("start")
def extract_text_from_pdf(pdf_path, tesseract_cmd=None):
    # Optional: Set tesseract command path
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    # Convert PDF to images (one image per page)
    print("image to pdf start")
    images = convert_from_path(pdf_path)
    print("image to pdf done")

    print("text extract start")
    full_text = ""
    for i, image in enumerate(images):
        print(f"Processing page {i + 1}...")
        text = pytesseract.image_to_string(image)
        full_text += f"\n\n--- Page {i + 1} ---\n{text}"
    print("text extract done")
    return full_text

if __name__ == "__main__":
    pdf_path = "test_images/Bucknellian1990Aug31.pdf"  # Replace with  PDF path
    text = extract_text_from_pdf(pdf_path)
    file1 = open("/Users/kellenremley/Desktop/bucknellian/text.txt" , "w")
    file1.write(text)
    file1.close()


    print(text)

