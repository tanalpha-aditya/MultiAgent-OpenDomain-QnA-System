from Query_Modification.QueryModification import modified_query
from retrieval import (
    retrieve_with_sparse_methods,
    retrieve_with_dense_methods,
    combine_retrieval_results
)
from agents import execute_agent_searches
from answer_generation import generate_answers
from reranking import rerank_answers

class QAPipeline:
    def __init__(self):
        pass

    def process_query(self, query: str):
        """
        Process a query through the entire pipeline.
        
        Args:
            query: The input query string
            
        Returns:
            Dictionary containing the final answer and intermediate results
        """
        try:
            # Step 1: Query Modification using LLMs
            modified_query = modified_query(query)

            # Step 2: Parallel Retrieval Process
            # 2a. Traditional Retrieval Methods (TF-IDF & BM25)
            sparse_results = retrieve_with_sparse_methods(modified_query)

            # 2b. Dense Retrieval with Embedding Models
            dense_results = retrieve_with_dense_methods(modified_query)

            # 2c. Agent-based Searches
            agent_results = execute_agent_searches(query)

            # Step 3: Combine all retrieval results
            combined_results = combine_retrieval_results(
                sparse_results,
                dense_results,
                agent_results
            )

            # Step 4: Generate multiple answer candidates using LLMs
            answer_candidates = generate_answers(
                query=query,
                modified_query=modified_query,
                retrieved_content=combined_results
            )

            # Step 5: Re-rank the generated answers
            ranked_answers = rerank_answers(
                query=query,
                answer_candidates=answer_candidates
            )

            # Return the best answer and intermediate results
            return {
                'original_query': query,
                'modified_query': modified_query,
                'retrieval_results': combined_results,
                'answer_candidates': answer_candidates,
                'ranked_answers': ranked_answers,
                'best_answer': ranked_answers[0] if ranked_answers else None
            }

        except Exception as e:
            raise

def main():
    # Example configuration
    config = {
        'llm_model': 'your_llm_model_name',
        'embedding_model': 'your_embedding_model_name',
        'max_results': 10,
        'reranking_threshold': 0.8
    }

    # Initialize the pipeline
    pipeline = QAPipeline(config)

    # Example usage
    query = "What is the capital of France?"
    try:
        result = pipeline.process_query(query)
        print(f"Original Query: {result['original_query']}")
        print(f"Modified Query: {result['modified_query']}")
        print(f"Best Answer: {result['best_answer']}")
    except Exception as e:
        print(f"Pipeline execution failed: {str(e)}")

if __name__ == "__main__":
    main()