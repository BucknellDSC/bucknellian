import fitz  # PyMuPDF
import pandas as pd
import re
from unidecode import unidecode

pdf_path = "pdfs/b_1960-1961 pg 1 sample.pdf"
csv_output_path = "/Users/thaonguyen/Desktop/bucknellian/spans_tagged.csv"
columns = ['page', 'xmin', 'ymin', 'xmax', 'ymax', 'text', 'is_upper', 'is_bold', 'span_font', 'font_size']

def extract_spans(pdf_path):
    doc = fitz.open(pdf_path)
    block_dict = {}

    for page_num, page in enumerate(doc, start=1):
        file_dict = page.get_text("dict")
        block_dict[page_num] = file_dict["blocks"]
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
    doc.close()
    return pd.DataFrame(rows, columns=columns)

# Define score and tag function
def tag_span(row, paragraph_font_size):
    score = row['font_size']

    if row['is_bold']:
        score += 1
    if row['is_upper'] and re.match(r"^[A-Z\s,.'-]+$", row['text']):
        score += 2  # stronger boost for fully uppercase clean text

    if score >= paragraph_font_size + 2 or (row['is_upper'] and row['is_bold']):
        return 'h'  # heading
    elif row['font_size'] == paragraph_font_size:
        return 'p'  # paragraph
    else:
        return 's'  # subtext

def main():
    print("Extracting spans from PDF...")
    span_df = extract_spans(pdf_path)

    print("Tagging spans...")
    most_common_size = span_df['font_size'].mode().iloc[0]
    span_df['tag'] = span_df.apply(lambda row: tag_span(row, most_common_size), axis=1)

    print("Saving tagged spans...")
    span_df.to_csv(csv_output_path, index=False)
    print("Done! Tagged span data saved to:", csv_output_path)


if __name__ == "__main__":
    main()