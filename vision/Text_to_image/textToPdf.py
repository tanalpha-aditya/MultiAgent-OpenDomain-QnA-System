from fpdf import FPDF
from datetime import datetime
import os

def create_pdf(input_text):
    # Create instance of FPDF class
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", size=10)
    
    # Split the input text into multiple lines if necessary
    # This ensures that the text fits the page and multiple pages are handled
    pdf.multi_cell(0, 5, txt=input_text)
    
    # Create a unique file name with the current time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"PDFs/Aditya_{timestamp}.pdf"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    # Save the PDF
    pdf.output(file_name)
    
    # Return the file path
    return file_name