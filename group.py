import pandas as pd
from dataframe import extract_spans  # Import the extract_spans function
import textwrap

# Define paths
pdf_path = "pdfs/b_1960-1961 pg 1 sample.pdf"
csv_output_path = "/Users/thaonguyen/Desktop/bucknellian/spans_tagged.csv"
headings_csv_output = "/Users/thaonguyen/Desktop/bucknellian/headings_and_content.csv"
headings_text_output = "/Users/thaonguyen/Desktop/bucknellian/headings_and_content.txt"

def group_headings_and_content(span_df):
    sections = []
    current_heading = None
    current_content = ""

    for _, row in span_df.iterrows():
        if row['tag'] == 'h':
            if current_heading:
                sections.append({
                    "heading": current_heading,
                    "content": current_content.strip()
                })
            current_heading = row['text']
            current_content = ""
        elif row['tag'] in ['p', 's'] and current_heading:
            current_content += row['text'] + " "

    if current_heading:
        sections.append({
            "heading": current_heading,
            "content": current_content.strip()
        })

    return pd.DataFrame(sections)

def write_head_content_to_text(headings_csv_output):
    df = pd.read_csv(headings_csv_output)

    # Replace NaN values in the 'content' column with an empty string
    df['content'] = df['content'].fillna("")

    with open(headings_text_output, "w", encoding="utf-8") as text_file:
        for _, row in df.iterrows():
            text_file.write(f"Heading: {row['heading']}\n")
            
            # Wrap and indent the content
            wrapped_content = textwrap.fill(
                str(row['content']),
                width=80,
                subsequent_indent="    " 
            )
            text_file.write(f"Content: {wrapped_content}\n")
            text_file.write("\n")

def main():
    span_df = pd.read_csv(csv_output_path)

    grouped_df = group_headings_and_content(span_df)
    grouped_df.to_csv(headings_csv_output, index=False)

    print("Done! Grouped headings and content saved to:", headings_csv_output)

    write_head_content_to_text(headings_csv_output)
    print("Done! Grouped headings and content saved to:", headings_text_output)

if __name__ == "__main__":
    main()