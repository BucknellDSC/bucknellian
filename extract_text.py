import fitz  # PyMuPDF library

# Path to the PDF file
ex_path = "pdfs/b_1960-1961 pg 1 sample.pdf"

#output_text.txt
doc = fitz.open(ex_path)
for page in doc:
    text = page.get_text()
    print(text)
doc.close()

# # Open the PDF document
# try:
#     doc = fitz.open(ex_path)
#     for page_num, page in enumerate(doc, start=1):
#         # Extract text from each page
#         text = page.get_text()
#         print(f"--- Page {page_num} ---")
#         print(text)
#         print("\n")
# finally:
#     # Ensure the document is closed properly
#     doc.close()