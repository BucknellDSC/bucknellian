import cv2
import numpy as np
import fitz  # PyMuPDF
from PIL import Image
import io
import time

def find_title_in_pdf(pdf_path, title_image_path, threshold=0.25):
    """
    Search for the title image in a PDF document and return the page numbers where it's found.
    threshold (float): Matching threshold (0-1), higher means more strict matching
    """

    # Load the title image trying to search for
    title_img = cv2.imread(title_image_path, cv2.IMREAD_COLOR)
    if title_img is None:
        raise ValueError(f"Could not load title image from {title_image_path}")
    
    print("PDF Loaded")

    # Convert to grayscale
    title_gray = cv2.cvtColor(title_img, cv2.COLOR_BGR2GRAY)
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    matching_pages = []
    
    print("Starting Image Recognition")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        
        # Convert PDF page to OpenCV image
        img_bytes = pix.tobytes("png")
        img_pil = Image.open(io.BytesIO(img_bytes))
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Perform template matching
        res = cv2.matchTemplate(img_gray, title_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        
        # If we found matches, add this page (1-indexed)
        if len(loc[0]) > 0:
            matching_pages.append(page_num + 1)

    print("End Image Recognition")
    
    doc.close()
    return matching_pages

if __name__ == "__main__":
    start_time_total = time.time()
    start_time_cpu = time.process_time()

    pdf_file = "/Users/kellenremley/Desktop/bucknellian/newspapers/Bucknellian_1990-1991.pdf" #"test_images/bucknellian_Nov8_to_Dec6_1920.pdf"
    title_image = "test_images/1990Title2.png" #"test_images/1920Nov8Title.png"
    found_pages = find_title_in_pdf(pdf_file, title_image)
    if found_pages:
        print(f"Title found on pages: {', '.join(map(str, found_pages))}")
    else:
        print("Title image not found in the PDF")

    end_time_total = time.time()
    end_time_cpu = time.process_time()
    print(f"Execution Time: {end_time_total - start_time_total} seconds")
    print(f"CPU Execution Time: {end_time_cpu - start_time_cpu} seconds")
