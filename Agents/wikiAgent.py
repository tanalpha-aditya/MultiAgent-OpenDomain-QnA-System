import wikipediaapi
from typing import List, Dict
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class WikiSearchResult:
    """Data class to store Wikipedia article information"""
    title: str
    summary: str
    full_text: str
    url: str
    last_modified: datetime
    categories: List[str]

def initialize_wikipedia_client(language: str = 'en', user_agent: str = 'WikipediaSearcher/1.0') -> wikipediaapi.Wikipedia:
    """
    Initialize Wikipedia API client
    
    Args:
        language: Language code (e.g., 'en' for English)
        user_agent: User agent string for API requests
        
    Returns:
        Wikipedia API client instance
    """
    return wikipediaapi.Wikipedia(
        language=language,
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent=user_agent
    )

def process_page(page: wikipediaapi.WikipediaPage) -> WikiSearchResult:
    """Process a Wikipedia page and extract relevant information"""
    categories = [cat.title for cat in page.categories.values()]
    
    return WikiSearchResult(
        title=page.title,
        summary=page.summary,
        full_text=page.text,
        url=page.fullurl,
        last_modified=datetime.strptime(page.touched, '%Y-%m-%dT%H:%M:%SZ'),
        categories=categories
    )

def search_wikipedia(client: wikipediaapi.Wikipedia, query: str, results_limit: int = 3) -> List[WikiSearchResult]:
    """
    Search Wikipedia and get detailed information for matching articles
    
    Args:
        client: Wikipedia API client instance
        query: Search query string
        results_limit: Maximum number of results to return
        
    Returns:
        List of WikiSearchResult objects containing article information
    """
    try:
        page = client.page(query)
        
        if not page.exists():
            logging.warning(f"No exact match found for: {query}")
            return []

        results = [process_page(page)]

        # Get related pages through links (if we want more results)
        if results_limit > 1:
            for link_title in list(page.links.keys())[:results_limit - 1]:
                link_page = client.page(link_title)
                if link_page.exists():
                    results.append(process_page(link_page))

        return results

    except Exception as e:
        logging.error(f"Error searching Wikipedia: {e}")
        return []

def format_result(result: WikiSearchResult, include_full_text: bool = False) -> str:
    """
    Format a search result for display
    
    Args:
        result: WikiSearchResult object to format
        include_full_text: Whether to include the full article text
        
    Returns:
        Formatted string containing article information
    """
    formatted = f"""
Title: {result.title}
URL: {result.url}
Last Modified: {result.last_modified}
Categories: {', '.join(result.categories[:5])}{'...' if len(result.categories) > 5 else ''}

Summary:
{result.summary}
"""
    if include_full_text:
        formatted += f"\nFull Text:\n{result.full_text}"
        
    return formatted

def get_wiki_data(query: str, results_limit: int = 3) -> List[WikiSearchResult]:
    """
    Get Wikipedia data for a given query
    
    Args:
        query: Search query string
        results_limit: Maximum number of results to return
        
    Returns:
        List of WikiSearchResult objects
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    client = initialize_wikipedia_client()
    return search_wikipedia(client, query, results_limit)

# # Example usage
# if __name__ == "__main__":
#     query = "Clash of Clans"
#     results = get_wiki_data(query, results_limit=3)
    
#     if not results:
#         print(f"No results found for query: {query}")
#     else:
#         for idx, result in enumerate(results, 1):
#             print(f"\nResult {idx}:")
#             print("-" * 60)
#             print(format_result(result))
