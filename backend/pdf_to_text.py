import PyPDF2
import re
import os
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"📖 PDF has {len(pdf_reader.pages)} pages")
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                
        print(f"✅ Extracted {len(text)} characters from PDF")
        return text
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return None

def split_by_chapters(text):
    """Split text by chapter headings"""
    # Common chapter patterns
    chapter_patterns = [
        r'Chapter\s+\d+[:\s]*([^\n]+)',  # Chapter 1: Introduction
        r'CHAPTER\s+\d+[:\s]*([^\n]+)',  # CHAPTER 1: INTRODUCTION
        r'\d+\.\s*([^\n]+)',             # 1. Introduction
        r'Part\s+\d+[:\s]*([^\n]+)',     # Part 1: Basics
        r'PART\s+\d+[:\s]*([^\n]+)',     # PART 1: BASICS
    ]
    
    chapters = []
    current_chapter = ""
    current_title = "Introduction"
    
    lines = text.split('\n')
    
    for line in lines:
        # Check if this line is a chapter heading
        is_chapter = False
        for pattern in chapter_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                # Save previous chapter
                if current_chapter.strip():
                    chapters.append({
                        'title': current_title,
                        'content': current_chapter.strip()
                    })
                
                # Start new chapter
                current_title = match.group(1).strip() if match.group(1) else match.group(0)
                current_chapter = line + "\n"
                is_chapter = True
                print(f"📑 Found chapter: {current_title}")
                break
        
        if not is_chapter:
            current_chapter += line + "\n"
    
    # Add the last chapter
    if current_chapter.strip():
        chapters.append({
            'title': current_title,
            'content': current_chapter.strip()
        })
    
    print(f"✅ Split into {len(chapters)} chapters")
    return chapters

def save_chapters_to_files(chapters, output_dir="data/chapters"):
    """Save chapters to individual text files"""
    os.makedirs(output_dir, exist_ok=True)
    
    for i, chapter in enumerate(chapters):
        filename = f"chapter_{i+1:02d}_{chapter['title'].replace(' ', '_').replace(':', '').replace('/', '_')[:50]}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {chapter['title']}\n")
            f.write("=" * 50 + "\n")
            f.write(chapter['content'])
        
        print(f"💾 Saved: {filename}")
    
    print(f"✅ Saved {len(chapters)} chapters to {output_dir}/")

def main():
    """Main function to convert PDF to text and split by chapters"""
    pdf_path = "data/Python Crash Course, 3rd Edition A Hands-On, Pr.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print("🔄 Converting PDF to text...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("❌ Failed to extract text from PDF")
        return
    
    print("🔄 Splitting by chapters...")
    chapters = split_by_chapters(text)
    
    if not chapters:
        print("❌ Failed to split into chapters")
        return
    
    print("🔄 Saving chapters to files...")
    save_chapters_to_files(chapters)
    
    print("🎉 PDF conversion complete!")
    print(f"📁 Chapters saved in: data/chapters/")

if __name__ == "__main__":
    main() 