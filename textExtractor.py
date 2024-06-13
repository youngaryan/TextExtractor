import fitz # PyMuPDF library
import pandas as pd 
import re
import logging
import sys

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextExtractor:
    
    def __init__(self, pdf_file_path, out_put_file_name, key_words):
        """
        Initialize the TextExtractor class with the PDF file path and output file name.
        """
        self.pdf_file_path = pdf_file_path
        self.out_put_file_name = out_put_file_name
        self.result_list = [] #list of (section_title, clause_number, clause_text, requirement_type)
        self.text = "" 
        self.section_titles = []
        self.key_words = key_words if key_words else ["must", "shall", "should"]  # Use default keywords if none provided
        self.title_detection_re_pattern = r"^(\d+)(\.)" #this pattern will match any string that starts with one or more digits, followed by a dot. e.g. "123.", "456.", "789."
        self.stentence_extraction_re_pattern =r'(?<!\d)\(\d+\)\s*(.*?)\.(?=\s*(?:\(\d+\)|\b|$))' #this pattern will match a string that starts with a parenthesis enclosed number (not preceded by a digit), followed by zero or more spaces, then any characters (as few as possible), and a dot. The dot must be followed by either a parenthesis enclosed number, or the end of the string.
    
    def __extract_text_from_pdf(self):
        """
        Extract text from the given PDF file.
        """
        try:
            doc = fitz.open(self.pdf_file_path)
            for page in doc:
                self.text += page.get_text()

            logging.info("Successfully read the data from the target file.")
        except fitz.FileNotFoundError as e:
            logging.error("FileNotFoundError occurred: %s", e)
            sys.exit(1) # exit
        except Exception as e:
            logging.error("An error occurred while reading the PDF file: %s", e)
            sys.exit(1) # exit

    def __parser(self):
        """
        Parse the extracted text data to identify sections and titles.
        """
        logging.info("Parsing the text data...")

        lines = self.text.split('\n')
        previous_line = None 
        previous_to_previous_line = None 
        section_texts = []
        section_text = ""

        for line in lines:
            if re.search(self.title_detection_re_pattern, line):
                if previous_line and previous_line[0].isupper():
                    self.section_titles.append(previous_line)
                elif previous_to_previous_line and previous_to_previous_line[0].isupper():
                    self.section_titles.append( previous_to_previous_line+" "+previous_line)
                else:
                    self.section_titles.append("No Section Title")

                section_texts.append(section_text + " ")
                section_text = "" 

            previous_to_previous_line = previous_line
            previous_line = line
            section_text+=line 

        if section_texts:
            section_texts.pop(0) # removing the introductions text

        return section_texts

    def __get_section_and_remove_section_number(self,sub_text):
        """
        Extract the section number from the text and remove it.
        """
        match = re.match(self.title_detection_re_pattern, sub_text)

        if match:
            section_number = match.group(1)
            sub_text = re.sub(self.title_detection_re_pattern, "", sub_text)

            return section_number, sub_text
        
        return None, None
    
    def __extract_sentences(self, sub_text):
        """
        Extract sentences from the text based on the given pattern.
        """
        matches = re.findall(self.stentence_extraction_re_pattern, sub_text, re.DOTALL)# It searches the sub_text for all matches of the pattern .
        return matches 
    

    def __classify_matches(self, clause_sentence):
        """
        Classify the sentences based on specific keywords.
        """
        classification = [word for word in self.key_words if word in clause_sentence]
        return ' / '.join(classification) if classification else None
   
    def __proccess_subtexts(self, sub_text, title_idx):
        """
        Process each section text to classify and store the clauses.
        """
        section_number, sub_text = self.__get_section_and_remove_section_number(sub_text)

        if not section_number or not sub_text:
            return self.result_list
        
        matches = self.__extract_sentences(sub_text)

        if matches:
            for i, sentence in enumerate(matches, start=1):
                classification = self.__classify_matches(sentence)
                if not classification:
                    continue
                self.result_list.append([self.section_titles[title_idx],section_number + '.'+str(i), sentence, classification])
        else:
            classification = self.__classify_matches(sub_text)
            if not classification:
                    return self.result_list
            self.result_list.append([self.section_titles[title_idx],section_number ,sub_text, classification])

        ## list of {section number, subsection number, the sentence, the type of requiements}
        return self.result_list


    def __save_to_csv(self):
        """
        Save the extracted and processed data to a CSV file.
        """
        try:
            # Convert the result list to a DataFrame
            df = pd.DataFrame(self.result_list, columns=['section','clause_number', 'clause_text', 'requirement_type'])
            logging.info("Successfully created the Data Frame.")
        except Exception as e:
            logging.error("Error creating DataFrame: %s", e)
            sys.exit(1) # exit

        try:
            # Write the DataFrame to a CSV file
            df.to_csv(self.out_put_file_name, index=False)
            logging.info("Successfully wrote the data to the CSV file.")
        except Exception as e:
            logging.error("Error writing to CSV file: %s", e)
            sys.exit(1) # exit    


    def run_extraction(self):
        """
        Run the full extraction process from PDF to CSV.
        """
        self.__extract_text_from_pdf()  # Extract text from the PDF file
        section_texts = self.__parser()  # Parse the extracted text


        for i in range(len(section_texts)):
            self.__proccess_subtexts(section_texts[i], i)  # Process each section of text

        self.__save_to_csv()  # Save the processed data to a CSV file
