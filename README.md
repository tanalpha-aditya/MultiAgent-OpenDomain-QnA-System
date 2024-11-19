# Multi-Agent Open-Domain QnA with Cross-Source Reranking  

**Team:** 13  
**Members:**  
- Aditya Raghuvanshi  
- Pranit Khanna  
- Yash Bhaskar  

Report Link : https://www.overleaf.com/read/pdhmfgwsmqmf#4bd790

---

## **Introduction**  

The objective of this project is to develop a multi-agent open-domain question-answering (ODQA) system capable of retrieving and synthesizing information from diverse sources. These sources include web searches, large language models (LLMs) such as **Llama 3**, and vision models for multi-modal retrieval. Leveraging datasets like **KILT**, **Natural Questions**, **HotspotQA**, **TriviaQA**, and **ELI5**, the system incorporates a **cross-source reranking model** to improve the selection of the most accurate answers. This project emphasizes scalability and reliability by addressing both context-free and context-based scenarios, even when confronted with an increasing volume of irrelevant documents.

---

## **Project Overview**  

- **Pipeline Development**: Created a multi-agent ODQA pipeline integrating specialized retrieval agents.  
- **Source Diversity**: Utilized web searches, LLMs, and vision models for retrieving information.  
- **Cross-Source Reranking**: Applied methods such as Reciprocal Rank Fusion (RRF) to enhance answer accuracy.  
- **Scalability Evaluation**: Tested the system on datasets with varying ratios of relevant and irrelevant documents.  

---

## **Pipeline**  

### **Dataset Construction**  

- **Mini-Wiki Collection**:  
   A condensed version of the Wikipedia dump was created by selecting a subset of documents relevant to the validation sets of **Natural Questions**, **HotspotQA**, **TriviaQA**, and **ELI5**.  

- **Document Ratio Variants**:  
   To evaluate retrieval scalability, multiple datasets with different relevant-to-irrelevant document ratios were constructed:  
   - **1:0**: Contains only 1000 relevant documents for 1000 queries.  
   - **1:1**: Contains 1000 relevant documents and 1000 irrelevant documents.  
   - **1:2**: Contains 1000 relevant documents and 2000 irrelevant documents.  

---

## **Retrieval Models**  

To ensure robust and efficient retrieval, the project combined sparse and dense methods:  

### **Sparse Retrieval Models**  

1. **TF-IDF**:  
   Measures the importance of terms in a document relative to the entire dataset.  
   - Effective for small datasets.  
   - Serves as a lightweight and interpretable baseline.  

2. **BM25**:  
   - Extends TF-IDF with term frequency normalization and length penalization.  
   - Handles query-document term overlap better than TF-IDF.  

3. **Bag of Words (BOW)**:  
   - A simple vector-space model using term frequency vectors.  
   - Acts as a baseline for comparison with more advanced methods.  

---

### **Dense Retrieval Models**  

1. **Text Embeddings (all-MiniLM-L6-v2)**:  
   - A pre-trained sentence-transformer for generating compact, high-quality embeddings.  
   - Captures semantic relationships between queries and documents.  
   - Lightweight and suitable for large-scale datasets.  

2. **Vision Embeddings (ViT)**:  
   - Generates embeddings for image-based data, enabling multi-modal information retrieval.  
   - Complements text-based retrieval for answering questions requiring visual context.  

---

## **Agents for Context Generation**  

### **Query Modification Agent**  
Refines user queries to optimize them for retrieval, ensuring that they are better suited for identifying relevant documents.  

### **Keyword Extraction Agent**  
Extracts key terms from the query and passes them to a **Wiki Agent**, which uses n-grams to retrieve relevant Wikipedia pages.  

### **Llama 3 Agent**  
Synthesizes context directly related to the user query, enriching the system’s ability to answer complex questions.  

---

## **Post-Retrieval Process**  

1. **Top-Ranked Document as Context**  
   The highest-ranked document was used directly as context for QnA tasks.  

2. **Iterative Use of Ranked Documents**  
   Explored answers using documents ranked in descending order of relevance.  

3. **Rank Fusion (RRF)**  
   Combined rankings from multiple retrieval methods (e.g., BM25, TF-IDF, MiniLM) to improve robustness and accuracy.  

---

## **Results and Evaluation**  

### **Retrieval Model Scores**  

| **Method**        | **Query Type** | **Ranking Scores** |  
|--------------------|----------------|---------------------|  
| **BOW**           | Modified       | 13.82 - 33.39      |  
| **BM25**          | Modified       | 736.74 - 785.09    |  
| **TF-IDF**        | Modified       | 730.61 - 788.87    |  
| **Vision**         | Modified       | 0.03 - 5.08        |  
| **MiniLM (Open)** | Modified       | 827.92 - 849.79    |  

### **Question Answering Model Scores**  

- **ROUGE Score**: Demonstrated improvements with RRF across most datasets.  
- **Cosine Similarity Score**: Highlighted semantic alignment in dense methods.  
- **BERT F1 Score**: Dense embeddings outperformed sparse methods.  

---

## **Analysis**  

1. **Sparse Models**:  
   - Sparse methods like **BM25** and **TF-IDF** performed well on context-free datasets but struggled with context-based tasks.  
   - **BOW** and **Vision** models were ineffective, worsening LLM performance compared to zero-shot baselines.  

2. **Dense Models**:  
   - Dense retrieval methods showed significant improvements in relevance and answer accuracy, especially when combining results with RRF.  

3. **Cross-Source Reranking**:  
   - RRF combining **BM25**, **TF-IDF**, and **MiniLM** yielded the best results.  
   - Using LLMs as rerankers was less reliable, with a bias toward zero-shot outputs.  

---

## **Conclusion**  

The multi-agent ODQA system successfully integrates sparse and dense retrieval methods, leveraging RRF for cross-source reranking. Dense methods and generative agents like **Llama 3** significantly enhance the system’s capability in open-domain settings. Future work can focus on improving multi-modal integration and reducing biases in LLM-based reranking.  