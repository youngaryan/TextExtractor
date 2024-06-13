import argparse
from textExtractor import TextExtractor

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="Extract text from a PDF and save to a CSV. To run this program, you must have Python installed along with the PyMuPDF and pandas libraries. To install these libraries, run the following commands respectively: 1- \"pip install PyMuPDF\" 2- \"pip install pandas\"")
    parser.add_argument("pdf_path", help="Path to the PDF file (must be provided).")
    parser.add_argument("output_path", help="Path to save the CSV file (must be provided).")
    parser.add_argument("key_words", nargs="*", help="Additional keywords for classification, if not provided the default keywords will be [must, shall, should] (optional).")
    args = parser.parse_args()

    # Create an instance of TextExtractor and run the extraction process
    extractor = TextExtractor(args.pdf_path, args.output_path, args.key_words)
    extractor.run_extraction()

if __name__ == "__main__":
    main()
