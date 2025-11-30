#!/usr/bin/env python3
"""
Debug script to check what content was generated for a specific PDF.
"""
import sys
import os

# Check if the PDF exists
pdf_file = "backend/static/learn_python_4d77b63b.pdf"

if os.path.exists(pdf_file):
    size = os.path.getsize(pdf_file)
    print(f"PDF File: {pdf_file}")
    print(f"Size: {size:,} bytes ({size/1024:.2f} KB)")
    
    if size < 10000:  # Less than 10KB
        print("\n⚠️  WARNING: PDF is very small (< 10KB)")
        print("This likely means the content generation failed or returned minimal data.")
        print("\nPossible causes:")
        print("1. Analyst agent returned minimal/empty content")
        print("2. Search agent failed to gather data")
        print("3. API token limit exceeded")
        print("4. JSON parsing error in analyst agent")
    else:
        print("\n✅ PDF size looks normal")
else:
    print(f"❌ PDF file not found: {pdf_file}")
