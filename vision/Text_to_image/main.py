# main.py
from textToPdf import create_pdf
from pdfToImage import pdf_to_image

def main():
    # Sample input text
    input_text = "This is a sample text that will be used to generate the PDF. " * 500  # Example long text
    
    # Call the create_pdf function and get the path of the generated PDF
    pdf_path = create_pdf(input_text)
    image_path = pdf_to_image(pdf_path)

    # Print the output path of the generated PDF
    print(f"PDF generated successfully: {pdf_path}")

    for i in image_path:
        print(i)

if __name__ == "__main__":
    main()
