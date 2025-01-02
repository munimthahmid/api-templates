import pdfplumber
from tabulate import tabulate
import os
import re

def text_to_paragraphs(text):
    """
    A simple heuristic to split text into paragraphs.
    Adjust as needed for your document structure.
    """
    # Split by double newlines or line breaks
    paragraphs = re.split(r"\n\s*\n+", text.strip())
    return paragraphs

def normalize_table_data(table):
    """
    Ensures each row in the table has the same number of columns
    by padding with empty strings if necessary.
    """
    # Find the maximum number of columns in this table
    max_cols = max(len(row) for row in table)

    normalized_table = []
    for row in table:
        # Pad the row to have max_cols columns
        row += [""] * (max_cols - len(row))
        normalized_table.append(row)

    return normalized_table

def convert_pdf_to_markdown(pdf_path, output_md_path=None):
    """
    Extracts text and tables from a PDF and converts them to Markdown,
    with improved table formatting.
    
    :param pdf_path: Path to the local PDF file
    :param output_md_path: Output path for the generated Markdown file (optional).
                           If None, will derive from `pdf_path` by appending ".md"
    :return: The Markdown text as a string.
    """
    if not output_md_path:
        # Derive a default Markdown path
        base, _ = os.path.splitext(pdf_path)
        output_md_path = base + ".md"

    markdown_lines = []

    # Open the PDF with pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            markdown_lines.append(f"# Page {page_number}")
            markdown_lines.append("")

            # 1. Extract raw text
            raw_text = page.extract_text() or ""
            if raw_text.strip():
                paragraphs = text_to_paragraphs(raw_text)
                for para in paragraphs:
                    markdown_lines.append(para.strip())
                    markdown_lines.append("")

            # 2. Extract tables
            # -- Try different table extraction modes if needed:
            #    tables = page.extract_tables(table_settings={"vertical_strategy": "lines",
            #                                                 "horizontal_strategy": "lines"})
            # For now, default is "stream" if lines are not explicitly used.
            tables = page.extract_tables()
            for i, table in enumerate(tables, start=1):
                # Skip empty table checks
                if not table or len(table) == 0:
                    continue

                markdown_lines.append(f"**Table {i}**")

                # Normalize rows (to handle missing columns in some rows)
                normalized_table = normalize_table_data(table)

                # We'll treat the first row as a header, if you want that:
                header = normalized_table[0]
                data = normalized_table[1:] if len(normalized_table) > 1 else []

                # Use tabulate in "pipe" format for cleaner Markdown columns
                # If you don't want a header, pass `header=None` or set `headers="firstrow"` to True if it actually is a header
                markdown_table = tabulate(data, headers=header, tablefmt="pipe")

                markdown_lines.append(markdown_table)
                markdown_lines.append("")  # blank line after table

            markdown_lines.append("---")  # Page separator
    
    # Join all lines into a single Markdown string
    md_output = "\n".join(markdown_lines)

    # Write to file
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(md_output)

    return md_output

if __name__ == "__main__":
    # Example usage
    input_pdf = "test2.pdf"  # Replace with your PDF file
    output_md = "sample_complex2.md"   # Replace with desired output markdown file name

    md_result = convert_pdf_to_markdown(input_pdf, output_md)
    print("Markdown extraction complete! Output written to:", output_md)
