import google.generativeai as genai
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AnalystAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def analyze_and_structure(self, topic: str, raw_data: str) -> Dict[str, Any]:
        logger.info(f"Analyzing topic '{topic}' and structuring ebook based on research data...")
        
        # Try up to 2 times (reduced from 3 for speed)
        for attempt in range(2):
            try:
                logger.info(f"Attempt {attempt + 1}/2 for topic '{topic}'")
                
                prompt = f"""
You are an expert researcher and author. Analyze the topic "{topic}" using the research data provided and create a comprehensive, topic-specific book.

TOPIC: {topic}

RESEARCH DATA:
{raw_data[:30000]}

INSTRUCTIONS:

1. READ THE RESEARCH DATA CAREFULLY
   - Understand what "{topic}" actually is from the research
   - Identify specific concepts, processes, and terminology
   - Note the key components and how they relate

2. CREATE TOPIC-SPECIFIC CHAPTERS
   - Base chapter titles on ACTUAL concepts from "{topic}"
   - DO NOT use generic names like "Introduction", "Basics", "Advanced"
   - Each chapter = one specific concept/process from "{topic}"
   - Use terminology from the research data
   - 6-8 chapters total

3. WRITE DETAILED CONTENT
   - Each chapter: 300-500 words
   - Use specific information from the research
   - Include real examples related to "{topic}"
   - Explain processes and concepts clearly
   - Add [IMAGE: specific description] only where truly helpful

4. ENSURE QUALITY
   - Every sentence must be about "{topic}"
   - Use proper terminology from the field
   - Make it educational and informative
   - Keep JSON valid (escape quotes properly)

EXAMPLE - If topic is "Photosynthesis":
- Chapter: "Chloroplast Structure and Function" (NOT "Chapter 1: Basics")
- Chapter: "Light-Dependent Reactions" (NOT "Understanding Photosynthesis")
- Chapter: "The Calvin Cycle Process" (NOT "Advanced Concepts")

YOUR TASK: Create a book about "{topic}" with chapters that reflect REAL concepts from the research.

OUTPUT (JSON):
{{
    "title": "Understanding {topic}",
    "author": "AI Research Author",
    "sections": [
        {{
            "title": "[Specific concept from {topic}]",
            "content": "[300-500 words about this concept]"
        }},
        ... (6-8 sections total)
    ]
}}

CRITICAL: Use ONLY information and terminology from "{topic}". Make it specific, not generic.
"""
                
                response = self.model.generate_content(
                    prompt, 
                    generation_config={
                        "response_mime_type": "application/json",
                        "temperature": 0.6,
                        "max_output_tokens": 6144  # Reduced for faster generation
                    }
                )
                
                # Try to parse JSON
                result = json.loads(response.text)
                
                # Validate the result
                sections = result.get('sections', [])
                logger.info(f"Generated book with {len(sections)} sections for '{topic}'")
                
                # Check if we have enough content
                if len(sections) < 4:
                    logger.warning(f"Only {len(sections)} sections generated for '{topic}'. Retrying...")
                    continue
                
                # Check if content looks generic
                first_section_content = sections[0].get('content', '') if sections else ''
                if 'This guide covers' in first_section_content or len(first_section_content) < 150:
                    logger.warning(f"Content appears generic for '{topic}'. Retrying...")
                    continue
                
                # Log chapter titles
                logger.info(f"Chapters for '{topic}':")
                for i, section in enumerate(sections):
                    title = section.get('title', 'Untitled')
                    logger.info(f"  {i+1}. {title}")
                
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed on attempt {attempt + 1} for '{topic}': {e}")
                if attempt < 1:
                    logger.info(f"Retrying...")
                    continue
                else:
                    raise Exception(f"Failed to parse content for '{topic}' after 2 attempts. The AI response was not valid JSON.")
                    
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1} for '{topic}': {e}")
                if attempt < 1:
                    continue
                else:
                    raise Exception(f"Failed to generate content for '{topic}': {str(e)}")
        
        # Should not reach here
        raise Exception(f"Failed to generate content for '{topic}' after all attempts.")
