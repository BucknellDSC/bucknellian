import pandas as pd
from dataframe import extract_spans  # Import the extract_spans function
import textwrap
import time  # Import the time module

# Define paths
csv_input_path = "/Users/thaonguyen/Desktop/bucknellian/outputs/csv_output/1990-1991_tagged_output.csv"
headings_csv_output = "/Users/thaonguyen/Desktop/bucknellian/outputs/csv_output/1990-1991_headings_and_content.csv"
headings_text_output = "/Users/thaonguyen/Desktop/bucknellian/outputs/txt_output/1990-1991_headings_and_content.txt"

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
            if pd.notnull(row['text']):
                current_content += str(row['text']) + " "


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
    start_time = time.time()

    # Read CSV file
    span_df = pd.read_csv(csv_input_path)

    # Group headings and content
    grouped_df = group_headings_and_content(span_df)
    grouped_df.to_csv(headings_csv_output, index=False)
    print("Done! Grouped headings and content saved to:", headings_csv_output)

    # Write headings and content to txt
    write_head_content_to_text(headings_csv_output)
    print("Done! Grouped headings and content saved to:", headings_text_output)

    end_time = time.time()

    # Elapsed time
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60
    print(f"Execution time: {minutes} minutes and {seconds:.2f} seconds")

    # Execution time to a CSV file
    execution_time_csv = "/Users/thaonguyen/Desktop/bucknellian/outputs/group_execution_time.csv"
    try:
        # Append to the CSV file if it exists, otherwise create it
        with open(execution_time_csv, "a", encoding="utf-8") as file:
            if file.tell() == 0:
                file.write("Input File,Minutes,Seconds\n")
            file.write(f"{csv_input_path},{minutes},{seconds:.2f}\n")
    except Exception as e:
        print(f"Error writing to execution time CSV: {e}")
    print(f"Execution time saved to: {execution_time_csv}")

if __name__ == "__main__":
    main()