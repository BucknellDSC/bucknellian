import fitz  # PyMuPDF
import pandas as pd
import re
from unidecode import unidecode

# Load  PDF
doc = fitz.open("pdfs/b_1960-1961 pg 1 sample.pdf")

block_dict = {}
for page_num, page in enumerate(doc, start=1):
    file_dict = page.get_text("dict")
    block_dict[page_num] = file_dict["blocks"]

# Create a dataframe for spans
columns = ['page', 'xmin', 'ymin', 'xmax', 'ymax', 'text', 'is_upper', 'is_bold', 'span_font', 'font_size']
rows = []

for page_num, blocks in block_dict.items():
    for block in blocks:
        if block['type'] == 0:  # Text block
            for line in block['lines']:
                for span in line['spans']:
                    xmin, ymin, xmax, ymax = list(span['bbox'])
                    font_size = span['size']
                    span_font = span['font']
                    text = unidecode(span['text']).strip()

                    if not text:
                        continue  # skip empty strings

                    is_bold = "bold" in span_font.lower()
                    is_upper = re.sub(r"[\(\[].*?[\)\]]", "", text).isupper()

                    rows.append((
                        page_num,
                        xmin, ymin, xmax, ymax,
                        text,
                        is_upper,
                        is_bold,
                        span_font,
                        font_size
                    ))

# Build DataFrame
span_df = pd.DataFrame(rows, columns=columns)

# Save to CSV file
span_df.to_csv("/Users/thaonguyen/Desktop/bucknellian/spans.csv", index=False)


most_common_size = span_df['font_size'].mode().iloc[0]

# Define score and tag function
def tag_span(row, paragraph_font_size):
    score = row['font_size']
    # Boost score for styling
    if row['is_bold']:
        score += 1
    if row['is_upper'] and re.match(r"^[A-Z\s,.'-]+$", row['text']):
        score += 2  # stronger boost for fully uppercase clean text

    # Apply tagging rules
    if score >= paragraph_font_size + 2 or (row['is_upper'] and row['is_bold']):
        return 'h'  # heading
    elif row['font_size'] == paragraph_font_size:
        return 'p'  # paragraph
    else:
        return 's'  # subtext

# Apply tag
span_df['tag'] = span_df.apply(lambda row: tag_span(row, most_common_size), axis=1)


span_df.to_csv("/Users/thaonguyen/Desktop/bucknellian/spans_tagged.csv", index=False)
