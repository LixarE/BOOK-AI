from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchAgent:
    def __init__(self):
        pass

    def search_and_scrape(self, topic: str, num_results: int = 5) -> str:
        logger.info(f"Searching for: {topic}")
        urls = []
        
        # Try DuckDuckGo search with retry
        for attempt in range(3):
            try:
                logger.info(f"Search attempt {attempt + 1}/3")
                results = DDGS().text(topic, max_results=num_results)
                if results:
                    for r in results:
                        if 'href' in r:
                            urls.append(r['href'])
                    break
                else:
                    logger.warning(f"No results on attempt {attempt + 1}")
                    time.sleep(2)  # Wait before retry
            except Exception as e:
                logger.error(f"Search attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    time.sleep(2)  # Wait before retry
                continue

        logger.info(f"Found {len(urls)} URLs: {urls[:3] if urls else 'none'}...")
        
        # If no URLs found, return fallback content
        if not urls:
            logger.warning("No URLs found after all attempts. Using fallback content.")
            return self._generate_fallback_content(topic)

        combined_content = ""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        successful_scrapes = 0
        for url in urls:
            try:
                logger.info(f"Scraping: {url}")
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch {url}: Status {response.status_code}")
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Extract text from paragraphs and headings
                text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])
                text = "\n".join([elem.get_text().strip() for elem in text_elements if elem.get_text().strip()])
                
                if not text.strip():
                    logger.warning(f"No text found in {url}")
                    continue

                # Limit content per URL
                combined_content += f"\n\n--- Source: {url} ---\n{text[:3000]}"
                successful_scrapes += 1
                
                # Add small delay to avoid rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to scrape {url}: {e}")
                continue
        
        logger.info(f"Successfully scraped {successful_scrapes}/{len(urls)} URLs")
        
        # If we got some content, return it
        if combined_content.strip():
            return combined_content
        
        # Otherwise, use fallback
        logger.warning("No content scraped. Using fallback content.")
        return self._generate_fallback_content(topic)
    
    def _generate_fallback_content(self, topic: str) -> str:
        """Generate basic fallback content when search fails"""
        return f"""
        Topic: {topic}
        
        Note: Web search was unable to gather external data. The AI will generate comprehensive content 
        based on its training data and knowledge about {topic}.
        
        This ebook will cover:
        - Introduction to {topic}
        - Fundamental concepts and principles
        - Key components and features
        - Practical applications and examples
        - Best practices and recommendations
        - Advanced topics and techniques
        - Common challenges and solutions
        - Resources for further learning
        
        The content will be generated using AI knowledge to provide a comprehensive learning resource.
        """
