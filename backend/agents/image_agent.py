import google.generativeai as genai
import logging
import re

logger = logging.getLogger(__name__)

class ImageAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def generate_images(self, book_data: dict) -> dict:
        logger.info("Generating images/diagrams...")
        
        for section in book_data.get("sections", []):
            content = section.get("content", "")
            # Find all image placeholders
            placeholders = re.findall(r'\[IMAGE: (.*?)\]', content)
            
            for desc in placeholders:
                logger.info(f"Generating image for: {desc}")
                # We will generate an SVG for diagrams/graphs
                # For realistic images, we might need a different model, but SVG is safe for "graphs, diagrams"
                
                prompt = f"""
                Create a simple, professional SVG diagram for: "{desc}"
                
                Requirements:
                - Return ONLY the SVG code, no markdown, no explanations
                - Use viewBox for responsiveness
                - Set width="600" height="400" for consistent sizing
                - Use clear, readable fonts (Arial, sans-serif)
                - Use a professional color scheme (blues, grays, black text)
                - Make it simple and clear
                - Include labels and text where appropriate
                
                Example format:
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400">
                  <!-- Your diagram here -->
                </svg>
                """
                
                try:
                    response = self.model.generate_content(prompt)
                    svg_code = response.text.strip()
                    
                    # Clean up the SVG code
                    svg_code = svg_code.replace("```svg", "").replace("```", "").strip()
                    
                    # Ensure it's valid SVG
                    if "<svg" in svg_code and "</svg>" in svg_code:
                        # Extract just the SVG part
                        svg_start = svg_code.find("<svg")
                        svg_end = svg_code.find("</svg>") + 6
                        svg_code = svg_code[svg_start:svg_end]
                        
                        # Ensure xmlns is present for PDF rendering
                        if 'xmlns=' not in svg_code:
                            svg_code = svg_code.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"')
                        
                        # Replace placeholder with properly formatted SVG
                        svg_html = f"""
<div class="image-container">
    {svg_code}
</div>
<p class="caption">Figure: {desc}</p>
"""
                        content = content.replace(f"[IMAGE: {desc}]", svg_html)
                        logger.info(f"Successfully generated SVG for: {desc}")
                    else:
                        # Failed to generate valid SVG, remove placeholder
                        logger.warning(f"Invalid SVG generated for: {desc}")
                        content = content.replace(f"[IMAGE: {desc}]", "")
                        
                except Exception as e:
                    logger.error(f"Image generation failed for {desc}: {e}")
                    content = content.replace(f"[IMAGE: {desc}]", "")
            
            section["content"] = content
            
        return book_data
