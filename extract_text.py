import fitz  # "top-level Python import name of the PyMuPDF library"

ex_path = "pdfs/b_1960-1961 pg 1 sample.pdf"
doc = fitz.open(ex_path)
for page in doc:
    text = page.get_text()
    print(text)
doc.close()