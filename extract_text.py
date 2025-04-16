import fitz  # PyMuPDF library

# Path to the PDF file
ex_path = "pdfs/b_1960-1961 pg 1 sample.pdf"

# output_text.txt and output_block.txt
doc = fitz.open(ex_path)
for page in doc:
    text = page.get_text()
    print(text)
doc.close()
