import os
from tqdm import tqdm
import numpy as np
from transformers import ViTModel, ViTFeatureExtractor, ViTImageProcessor
from PIL import Image
import re
from fpdf import FPDF
from datetime import datetime
import fitz
import joblib
import json

model = ViTModel.from_pretrained('google/vit-base-patch16-224-in21k')
processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')

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
    file_name = f"temp/PDFs/{timestamp}.pdf"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    # Save the PDF
    pdf.output(file_name)
    
    # Return the file path
    return file_name

def pdf_to_image(pdf_path, zoom=2.0):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Create a list to store image paths
    image_paths = []
    
    # Create an 'Images' directory if it doesn't exist
    os.makedirs("temp/Images", exist_ok=True)
    
    # Iterate over PDF pages and convert each to an image
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Load the page
        
        # Set zoom level to improve quality
        mat = fitz.Matrix(zoom, zoom)  # Create a transformation matrix with the zoom level
        pix = page.get_pixmap(matrix=mat)  # Render the page to an image with the specified zoom
        
        image_file = f'temp/Images/{os.path.basename(pdf_path)}_page_{page_num}.png'
        pix.save(image_file)  # Save the image as PNG
        image_paths.append(image_file)
    
    # Return the list containing paths of all images
    return image_paths

def sanitize_text(text):
    """
    Cleans and standardizes text by keeping only alphanumeric characters and spaces.
    Args:
        text (str): Text to sanitize.
    Returns:
        str: Sanitized text.
    """
    if isinstance(text, str):
        # Use regex to keep only alphanumeric characters and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Optionally, collapse multiple spaces into a single space
        text = re.sub(r'\s+', ' ', text).strip()
    return text

def text_to_images(text):
    text = sanitize_text(text)
    pdf_path = create_pdf(text)
    image_paths = pdf_to_image(pdf_path)
    return image_paths

def documents_to_images(path):
    document_set = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                content = f.read()
                document_set.append(content)
    document_image_paths = []
    for document in document_set:
        image_paths = text_to_images(document)
        document_image_paths.append(image_paths)
    return document_image_paths

def single_unit_embedding(text):
    image_paths = text_to_images(text)
    temp = []
    for image_path in image_paths:
        image = Image.open(image_path)
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        vector = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        temp.append(vector)
    return np.mean(np.array(temp), axis=0)

def single_image_embedding(image):
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    vector = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return vector

def documents_to_vision_embeddings(documents):
    document_vision_embeddings = []
    for document in tqdm(documents):
        vector = single_unit_embedding(document)
        document_vision_embeddings.append(vector)
    return document_vision_embeddings

def queries_to_vision_embeddings(queries):
    query_vision_embeddings = []
    for query in tqdm(queries):
        vector = single_unit_embedding(query)
        query_vision_embeddings.append(vector)
    return query_vision_embeddings

def get_documents_from_scores(scores):
    rankings = []
    for score in scores:
        rankings.append(score[0])
    return rankings

def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    if(np.linalg.norm(v1) != 0 and np.linalg.norm(v2) != 0):
        sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    else:
        sim = 0
    return sim

def vision_rankings(query_embedding, document_embeddings, k):
    # query_embedding = single_unit_embedding(query)
    scores = []
    for idx, embedding in enumerate(document_embeddings):
        scores.append((idx, cosine_similarity(query_embedding[0], embedding[0])))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = scores[:k]
    rankings = get_documents_from_scores(scores)
    return rankings, scores


def vision_pipeline(query, document_embeddings_path="Retrieval/savedModels/document-vision-embeddings.json", ids_path="Retrieval/savedModels/ids.pkl", k=100):
    # document_embeddings = joblib.load(document_embeddings_path)
    ids = joblib.load(ids_path)
    with open(document_embeddings_path, "r") as f:
        document_vision_embeddings2 = json.load(f)
    document_vision_embeddings = []
    for embedding in tqdm(document_vision_embeddings2):
        document_vision_embeddings.append(np.array(embedding))
    print("loaded embeddings")
    query_embedding = single_unit_embedding(query)
    rankings, scores = vision_rankings(query_embedding, document_vision_embeddings, k)
    rankings2 = []
    for ranking in rankings:
        rankings2.append(ids[ranking])
    return rankings2