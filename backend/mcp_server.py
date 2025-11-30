from mcp.server.fastmcp import FastMCP
import os
import asyncio
from dotenv import load_dotenv
from .agents.workflow import EbookWorkflow

# Load environment variables
load_dotenv(dotenv_path="backend/.env")

# Initialize FastMCP server
mcp = FastMCP("Ebook Generator")

@mcp.tool()
async def generate_ebook(topic: str) -> str:
    """
    Generates a comprehensive PDF ebook on the given topic.
    
    Args:
        topic: The subject matter of the ebook (e.g., "Introduction to Python").
        
    Returns:
        A message indicating success and the path to the generated PDF.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment variables."

    workflow = EbookWorkflow(api_key)
    try:
        # Run the workflow
        result = await workflow.run(topic)
        
        # Return a user-friendly message
        pdf_path = result.get("pdf_path")
        filename = result.get("filename")
        return f"Successfully generated ebook '{filename}'. Available at: backend/{pdf_path}"
    except Exception as e:
        return f"Error generating ebook: {str(e)}"

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
