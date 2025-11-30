import markdown
import logging
import base64

logger = logging.getLogger(__name__)

class FormatterAgent:
    def __init__(self):
        pass

    def format_to_html(self, book_data: dict) -> str:
        logger.info("Formatting book to HTML...")
        
        title = book_data.get("title", "Untitled Book")
        author = book_data.get("author", "AI Author")
        sections = book_data.get("sections", [])
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-family: 'Helvetica', 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    font-size: 11pt;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                    page-break-after: avoid;
                }}
                h1 {{
                    font-size: 24pt;
                    margin-bottom: 1rem;
                }}
                h2 {{
                    font-size: 18pt;
                    margin-top: 2rem;
                    margin-bottom: 1rem;
                }}
                h3 {{
                    font-size: 14pt;
                    margin-top: 1.5rem;
                    margin-bottom: 0.75rem;
                }}
                .title-page {{
                    text-align: center;
                    padding-top: 5cm;
                    page-break-after: always;
                }}
                .chapter {{
                    page-break-before: always;
                }}
                .image-container {{
                    margin: 2rem auto;
                    text-align: center;
                    page-break-inside: avoid;
                }}
                .image-container svg {{
                    max-width: 100%;
                    height: auto;
                    display: inline-block;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 10px;
                    background: white;
                }}
                .caption {{
                    text-align: center;
                    font-style: italic;
                    font-size: 9pt;
                    color: #666;
                    margin-top: 0.5rem;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 1rem;
                    border-radius: 5px;
                    overflow-x: auto;
                    font-size: 9pt;
                    page-break-inside: avoid;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 0.2rem 0.4rem;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    font-size: 9pt;
                }}
                p {{
                    margin-bottom: 0.75rem;
                    text-align: justify;
                }}
                ul, ol {{
                    margin-bottom: 1rem;
                    margin-left: 2rem;
                }}
                li {{
                    margin-bottom: 0.5rem;
                }}
            </style>
        </head>
        <body>
            <div class="title-page">
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">{title}</h1>
                <p style="font-size: 1.5rem;">By {author}</p>
            </div>
        """
        
        for section in sections:
            sec_title = section.get("title", "")
            sec_content = section.get("content", "")
            
            # Convert markdown content to HTML
            # The content already has SVG embedded from ImageAgent
            html_body = markdown.markdown(
                sec_content,
                extensions=['fenced_code', 'tables', 'nl2br']
            )
            
            html_content += f"""
            <div class="chapter">
                <h2>{sec_title}</h2>
                <div class="content">
                    {html_body}
                </div>
            </div>
            """
            
        html_content += """
        </body>
        </html>
        """
        
        logger.info("HTML formatting complete")
        return html_content
