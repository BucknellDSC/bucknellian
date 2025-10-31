import fitz  # PyMuPDF library

# Path to the PDF file
ex_path = "pdfs/b_1960-1961 pg 1 sample.pdf"

doc = fitz.open(ex_path)
for page in doc:
    blocks = page.get_text("blocks")
    for block in blocks:
        if block[6] == 0:  # We only take the text
            print("\n")
            print(block[4])

doc.close()
