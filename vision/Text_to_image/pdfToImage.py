import fitz  # PyMuPDF
import os

def pdf_to_image(pdf_path, zoom=2.0):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Create a list to store image paths
    image_paths = []
    
    # Create an 'Images' directory if it doesn't exist
    os.makedirs("Images", exist_ok=True)
    
    # Iterate over PDF pages and convert each to an image
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Load the page
        
        # Set zoom level to improve quality
        mat = fitz.Matrix(zoom, zoom)  # Create a transformation matrix with the zoom level
        pix = page.get_pixmap(matrix=mat)  # Render the page to an image with the specified zoom
        
        image_file = f'Images/{os.path.basename(pdf_path)}_page_{page_num}.png'
        pix.save(image_file)  # Save the image as PNG
        image_paths.append(image_file)
    
    # Return the list containing paths of all images
    return image_paths

# Example usage
# pdf_to_image('your_pdf_file.pdf', zoom=2.0)  # Increase zoom for higher quality
