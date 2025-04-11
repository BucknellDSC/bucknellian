import fitz  # PyMuPDF library

# Path to the PDF file
ex_path = "pdfs/b_1960-1961 pg 1 sample.pdf"

# # output_text.txt and output_block.txt
# doc = fitz.open(ex_path)
# for page in doc:
#     text = page.get_text()
#     print(text)
# doc.close()



# output page num
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



# chatgpt trying it out with page 8 and page 1
# doc = fitz.open(ex_path)
# page = doc[0]

# blocks = page.get_text("blocks")
# blocks = [b for b in blocks if b[4].strip()]  # remove empty blocks

# # Define threshold for column split (tweak if needed)
# split_x = 500

# left_text = []
# right_text = []

# for b in blocks:
#     text = b[4].replace('\n', ' ').strip()
#     if b[0] < split_x:
#         left_text.append(text)
#     else:
#         right_text.append(text)

# # Save to files or print
# with open("page8.txt", "w") as f:
#     f.write("\n".join(left_text))

# with open("page1.txt", "w") as f:
#     f.write("\n".join(right_text))

# doc.close()