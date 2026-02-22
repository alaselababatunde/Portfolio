import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from typing import List, Dict

class SearchTool:
    def __init__(self):
        self.ddgs = DDGS()

    def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        results = []
        try:
            # specifically prioritize dstv.com
            search_query = f"{query} site:dstv.com"
            with DDGS() as ddgs:
                for r in ddgs.text(search_query, max_results=max_results):
                    results.append({
                        "title": r['title'],
                        "link": r['href'],
                        "snippet": r['body']
                    })
        except Exception as e:
            print(f"Search error: {e}")
        return results

    def scrape_dstv_page(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            text = soup.get_text(separator=' ', strip=True)
            return text[:2000] # Return first 2000 chars for context
        except Exception as e:
            print(f"Scrape error: {e}")
            return ""

search_tool = SearchTool()
