from weasyprint import HTML
import os
import logging
import uuid

logger = logging.getLogger(__name__)

class PDFAgent:
    def __init__(self):
        self.output_dir = "backend/static"
        os.makedirs(self.output_dir, exist_ok=True)

    def create_pdf(self, html_content: str, topic: str) -> str:
        logger.info("Converting HTML to PDF...")
        
        # Sanitize filename
        safe_topic = "".join([c for c in topic if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
        filename = f"{safe_topic}_{uuid.uuid4().hex[:8]}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            HTML(string=html_content).write_pdf(filepath)
            logger.info(f"PDF saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"PDF creation failed: {e}")
            raise e
