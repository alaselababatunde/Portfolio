import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from typing import List, Dict

async def perform_web_search(query: str) -> str:
    """
    Performs a web search using DuckDuckGo and scrapes relevant UBA pages.
    """
    search_results = []
    
    # Add site restriction to prioritize UBA
    search_query = f"{query} site:ubagroup.com"
    
    try:
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=3)
            for r in results:
                search_results.append(f"Source: {r['href']}\nContent: {r['body']}")
    except Exception as e:
        print(f"Search error: {e}")

    # Fallback to general search if no results found on UBA site
    if not search_results:
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=3)
                for r in results:
                    search_results.append(f"Source: {r['href']}\nContent: {r['body']}")
        except Exception as e:
            print(f"Fallback search error: {e}")

    return "\n\n".join(search_results)

async def scrape_uba_website(url: str) -> str:
    """
    Scrapes a specific UBA website page for content.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text
                text = soup.get_text()
                # Break into lines and remove leading and trailing whitespace
                lines = (line.strip() for line in text.splitlines())
                # Break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # Drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
                return text[:2000] # Limit to 2000 chars
    except Exception as e:
        print(f"Scrape error: {e}")
    return ""
