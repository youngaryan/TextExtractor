# TextExtractor
In this repository, the TextExtractor is provided along with a sample PDF and CSV file.

# Overview
The TextExtractor class is designed to extract text from a PDF file, process the extracted text to identify and classify specific clauses based on given keywords, and save the processed data into a CSV file.

# Features
* Extracts text from a PDF file.
* Identifies sections and titles within the text.
* Extracts and dynamically classifies sentences based on given keywords.
* Saves the processed data into a CSV file.

# Requirements
* Python 3.x
* PyMuPDF (fitz) library
* pandas library

Install the required libraries using the following commands:

    
    pip install PyMuPDF
    pip install pandas
  

# Usage

  
    python script_name.py <pdf_path> <output_path> [key_words...]
   
    
* pdf_path: Path to the PDF file (must be provided).
* output_path: Path to save the CSV file (must be provided).
* key_words: Additional keywords for classification (optional). If not provided, the default keywords will be ["must", "shall", "should"].

  ![image](https://github.com/youngaryan/TextExtractor/assets/121689731/d563748e-b2ca-4876-a17c-f407c0a0d8fc)


# Example

    
*        python script_name.py sample.pdf output.csv
  
    ![image](https://github.com/youngaryan/TextExtractor/assets/121689731/c436c604-f0ab-4d21-8a31-17be89fc504f)
    
    ![image](https://github.com/youngaryan/TextExtractor/assets/121689731/39c1e7b0-b766-4f95-a1ea-3552e11cd915)


  
*      python script_name.py sample.pdf output.csv should shall
   
    ![image](https://github.com/youngaryan/TextExtractor/assets/121689731/7970894a-5bfc-45c6-a6cd-be4b01fd1d8e)
    
    ![image](https://github.com/youngaryan/TextExtractor/assets/121689731/a23bef33-fb77-43a1-887d-d22bc25cf770)


