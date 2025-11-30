#!/usr/bin/env python3
"""
Test script to verify PDF generation is working correctly.
"""
import asyncio
import sys
import os

sys.path.insert(0, '/run/media/lulu/New Volume/Code/Capstone Project- Book Writer/Ag_3')

from dotenv import load_dotenv
from backend.agents.workflow import EbookWorkflow

async def test_pdf_generation():
    """Test the PDF generation with a simple topic."""
    print("=" * 60)
    print("Testing PDF Generation")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv(dotenv_path="backend/.env")
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found")
        return False
    
    print("✅ API Key loaded")
    
    # Test topic
    test_topic = "Basic Math"
    print(f"\n📚 Testing with topic: '{test_topic}'")
    print("-" * 60)
    
    try:
        workflow = EbookWorkflow(api_key)
        print("\n🚀 Starting generation...")
        
        result = await workflow.run(test_topic)
        
        if result.get("status") == "success":
            pdf_path = result.get("pdf_path")
            filename = result.get("filename")
            full_path = f"backend/{pdf_path}"
            
            print(f"\n✅ SUCCESS!")
            print(f"   📄 PDF File: {filename}")
            print(f"   📁 Path: {full_path}")
            
            # Check file size
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                print(f"   📊 Size: {size:,} bytes ({size/1024:.1f} KB)")
                
                if size > 5000:  # More than 5KB
                    print("\n✅ PDF has content (size > 5KB)")
                    return True
                else:
                    print("\n⚠️  PDF might be empty (size < 5KB)")
                    return False
            else:
                print(f"\n❌ PDF file not found at {full_path}")
                return False
        else:
            print(f"\n❌ Generation failed: {result}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🧪 PDF Generation Test\n")
    success = asyncio.run(test_pdf_generation())
    
    if success:
        print("\n✨ Test PASSED - PDF generation is working!")
        sys.exit(0)
    else:
        print("\n⚠️  Test FAILED - Check errors above")
        sys.exit(1)
