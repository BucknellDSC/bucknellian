import pytesseract
from pdf2image import convert_from_path
import time
import os


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
    start_time_total = time.time()
    start_time_cpu = time.process_time()

    pdf_path = "/Users/kellenremley/Desktop/bucknellian/newspapers/Bucknellian_1980-1981.pdf" # Replace with  PDF path
    text = extract_text_from_pdf(pdf_path)
    file1 = open("/Users/kellenremley/Desktop/bucknellian/text/text80-81.txt" , "w")
    file1.write(text)
    file1.close()

    end_time_total = time.time()
    end_time_cpu = time.process_time()
    print(f"Execution Time: {end_time_total - start_time_total} seconds")
    print(f"CPU Execution Time: {end_time_cpu - start_time_cpu} seconds")

