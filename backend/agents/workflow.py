import logging
from .search_agent import SearchAgent
from .analyst_agent import AnalystAgent
from .image_agent import ImageAgent
from .formatter_agent import FormatterAgent
from .pdf_agent import PDFAgent
from .verifier_agent import VerifierAgent

logger = logging.getLogger(__name__)

class EbookWorkflow:
    def __init__(self, api_key: str):
        self.search_agent = SearchAgent()
        self.analyst_agent = AnalystAgent(api_key)
        self.image_agent = ImageAgent(api_key)
        self.formatter_agent = FormatterAgent()
        self.pdf_agent = PDFAgent()
        self.verifier_agent = VerifierAgent()

    async def run(self, topic: str) -> dict:
        logger.info(f"Starting workflow for topic: {topic}")
        
        # Step 1: Search
        raw_data = self.search_agent.search_and_scrape(topic)
        if not raw_data:
            raise Exception("Search failed to gather data.")

        # Retry loop for generation and verification
        max_retries = 3
        for attempt in range(max_retries):
            logger.info(f"Generation attempt {attempt + 1}/{max_retries}")
            
            # Step 2: Analyze
            book_data = await self.analyst_agent.analyze_and_structure(topic, raw_data)
            
            # Step 3: Images
            book_data_with_images = await self.image_agent.generate_images(book_data)
            
            # Step 4: Format
            html_content = self.formatter_agent.format_to_html(book_data_with_images)
            
            # Step 5: PDF
            try:
                pdf_path = self.pdf_agent.create_pdf(html_content, topic)
            except Exception as e:
                logger.error(f"PDF creation failed: {e}")
                continue # Retry
            
            # Step 6: Verify
            if self.verifier_agent.verify_pdf(pdf_path):
                # Success!
                # Return relative path for frontend
                relative_path = pdf_path.replace("backend/", "")
                return {
                    "status": "success",
                    "pdf_path": relative_path,
                    "filename": os.path.basename(pdf_path)
                }
            else:
                logger.warning("Verification failed. Retrying...")
                
        raise Exception("Failed to generate a valid PDF after 3 attempts.")
import os
