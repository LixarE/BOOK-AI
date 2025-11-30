import os
import logging

logger = logging.getLogger(__name__)

class VerifierAgent:
    def __init__(self):
        pass

    def verify_pdf(self, filepath: str) -> bool:
        logger.info(f"Verifying PDF: {filepath}")
        
        if not os.path.exists(filepath):
            logger.error("PDF file does not exist.")
            return False
            
        size = os.path.getsize(filepath)
        if size == 0:
            logger.error("PDF file is empty.")
            return False
            
        logger.info(f"PDF verified successfully. Size: {size} bytes.")
        return True
