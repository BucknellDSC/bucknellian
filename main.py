from opencvtest import find_title_in_pdf
from pytesseracttest import extract_text_from_pdf
import time
import re


if __name__ == "__main__":
    start_time_total = time.time()
    start_time_cpu = time.process_time()

    #opencvtest
    pdf_file = "test_images/bucknellian_Nov8_to_Dec6_1920.pdf"
    title_image = "test_images/1920Nov8Title.png"
    found_pages = find_title_in_pdf(pdf_file, title_image)
    if found_pages:
        print(f"Title found on pages: {', '.join(map(str, found_pages))}")
    else:
        print("Title image not found in the PDF")

    #pytesseract test
    pdf_path = "test_images/bucknellian_Nov8_to_Dec6_1920.pdf"  # Replace with  PDF path
    text = extract_text_from_pdf(pdf_path)
    
    ''' a attempt at using regular expression to do what code below does
    pages_pattern = "|".join(str(page) for page in found_pages)
    print(f"pages pattern {pages_pattern}")
    x = re.findall(rf"-- Page ({pages_pattern}) --", text) #  Research more on regular expression to solve this, does not work intended way only sees that there are matches doesnt get index of match
    print(x)
    '''
    pages_pattern = "|".join(str(page) for page in found_pages)
    for pn in pages_pattern:
        page_idx = text.find(f"-- Page {pn} --")
        print(f"Page {pn} is at index {page_idx}")
    

    file1 = open("/Users/kellenremley/Desktop/bucknellian/text.txt" , "w")
    file1.write(text)
    file1.close()

    end_time_total = time.time()
    end_time_cpu = time.process_time()
    print(f"Execution Time: {end_time_total - start_time_total} seconds")
    print(f"CPU Execution Time: {end_time_cpu - start_time_cpu} seconds")
