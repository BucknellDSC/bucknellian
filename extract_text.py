import fitz  # PyMuPDF

doc = fitz.open("pdfs/b_1960-1961 pg 1 sample.pdf")
for page in doc:
    text = page.get_text()
    print(text)
    
doc.close()