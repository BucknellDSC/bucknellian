import pandas as pd
from dataframe import extract_spans  # Import the extract_spans function

# Define paths
pdf_path = "pdfs/b_1960-1961 pg 1 sample.pdf"
csv_output_path = "/Users/thaonguyen/Desktop/bucknellian/spans_tagged.csv"
headings_csv_output = "/Users/thaonguyen/Desktop/bucknellian/headings_and_content.csv"

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

def main():
    span_df = pd.read_csv(csv_output_path)

    grouped_df = group_headings_and_content(span_df)
    grouped_df.to_csv(headings_csv_output, index=False)

    print("Done! Grouped headings and content saved to:", headings_csv_output)

if __name__ == "__main__":
    main()