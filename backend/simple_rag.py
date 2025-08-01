import os
import glob
import re
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleBookRAG:
    def __init__(self):
        self.chapters = []
        self.is_initialized = False
    
    def load_chapters(self):
        """Load all chapter files from the data/chapters directory"""
        chapters_dir = "data/chapters"
        if not os.path.exists(chapters_dir):
            logger.error(f"Chapters directory not found: {chapters_dir}")
            return []
        
        chapter_files = glob.glob(os.path.join(chapters_dir, "*.txt"))
        logger.info(f"Found {len(chapter_files)} chapter files")
        
        chapters = []
        for file_path in sorted(chapter_files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    filename = os.path.basename(file_path)
                    chapters.append({
                        'filename': filename,
                        'content': content,
                        'title': self.extract_title(content)
                    })
            except Exception as e:
                logger.warning(f"Error reading {file_path}: {e}")
        
        logger.info(f"Loaded {len(chapters)} chapters")
        return chapters
    
    def extract_title(self, content: str) -> str:
        """Extract title from chapter content"""
        lines = content.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            if line.startswith('Title:'):
                return line.replace('Title:', '').strip()
        return "Unknown Chapter"
    
    def initialize(self):
        """Initialize the simple RAG system"""
        try:
            logger.info("Loading chapters...")
            self.chapters = self.load_chapters()
            
            if not self.chapters:
                logger.error("No chapters loaded")
                return False
            
            self.is_initialized = True
            logger.info("✅ Simple RAG system initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing RAG system: {e}")
            return False
    
    def search_chapters(self, query: str, top_k: int = 3) -> List[Dict]:
        """Enhanced search that looks for code examples and better content"""
        query_lower = query.lower()
        query_words = [word for word in query_lower.split() if len(word) > 2]  # Filter short words
        
        results = []
        for chapter in self.chapters:
            content_lower = chapter['content'].lower()
            score = 0
            
            # Give higher weight to title matches
            title_lower = chapter['title'].lower()
            for word in query_words:
                if word in title_lower:
                    score += 10  # High weight for title matches
                if word in content_lower:
                    score += content_lower.count(word)
            
            # Bonus for exact phrase matches
            if query_lower in content_lower:
                score += 50
            
            # Bonus for code-related content
            if any(code_word in content_lower for code_word in ['def ', 'class ', 'import ', 'print(', 'if ', 'for ', 'while ', 'return ']):
                score += 20
            
            # Bonus for specific programming terms
            programming_terms = ['function', 'variable', 'loop', 'condition', 'string', 'list', 'dictionary', 'module']
            for term in programming_terms:
                if term in query_lower and term in content_lower:
                    score += 15
            
            if score > 0:
                results.append({
                    'chapter': chapter,
                    'score': score,
                    'title': chapter['title']
                })
        
        # Sort by score and return top results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def find_best_snippet(self, content: str, query: str, max_length: int = 1500) -> str:
        """Find the most relevant snippet with complete code examples"""
        query_lower = query.lower()
        content_lower = content.lower()
        
        # Look for complete code blocks first
        code_blocks = re.findall(r'```.*?```', content, re.DOTALL)
        if not code_blocks:
            # Look for function definitions with their full body
            code_blocks = re.findall(r'def\s+\w+\([^)]*\):.*?(?=\n\S|\Z)', content, re.DOTALL)
        if not code_blocks:
            # Look for class definitions
            code_blocks = re.findall(r'class\s+\w+.*?def', content, re.DOTALL)
        
        # If we found code blocks, include them with context
        if code_blocks:
            best_code = code_blocks[0]
            # Find the paragraph before the code
            lines = content.split('\n')
            code_start = content.find(best_code)
            if code_start > 0:
                # Get more context before the code
                before_code = content[:code_start].strip()
                if before_code:
                    # Take the last few paragraphs before the code
                    paragraphs = before_code.split('\n\n')
                    if paragraphs:
                        # Get the last 2-3 paragraphs for better context
                        context_paragraphs = paragraphs[-3:] if len(paragraphs) >= 3 else paragraphs
                        context = '\n\n'.join(context_paragraphs).strip()
                        result = f"{context}\n\n💻 Complete Code Example:\n{best_code}"
                        if len(result) > max_length:
                            result = result[:max_length] + "..."
                        return result
        
        # Look for specific code patterns in the content
        code_patterns = [
            r'def\s+\w+\([^)]*\):.*?(?=\n\S|\Z)',  # Function definitions
            r'class\s+\w+.*?def',  # Class definitions
            r'for\s+\w+\s+in\s+.*?:.*?(?=\n\S|\Z)',  # For loops
            r'if\s+.*?:.*?(?=\n\S|\Z)',  # If statements
            r'while\s+.*?:.*?(?=\n\S|\Z)',  # While loops
        ]
        
        for pattern in code_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                best_match = matches[0]
                # Find context before this code
                code_start = content.find(best_match)
                if code_start > 0:
                    before_code = content[:code_start].strip()
                    if before_code:
                        paragraphs = before_code.split('\n\n')
                        if paragraphs:
                            context = paragraphs[-1].strip()
                            result = f"{context}\n\n💻 Code Example:\n{best_match}"
                            if len(result) > max_length:
                                result = result[:max_length] + "..."
                            return result
        
        # Try to find a paragraph that contains the query and code
        paragraphs = content.split('\n\n')
        best_paragraph = ""
        best_score = 0
        
        for paragraph in paragraphs:
            if len(paragraph.strip()) < 50:  # Skip very short paragraphs
                continue
                
            score = 0
            for word in query_lower.split():
                if word in paragraph.lower():
                    score += paragraph.lower().count(word)
            
            # High bonus for code in paragraph
            if any(code_indicator in paragraph for code_indicator in ['def ', 'class ', 'import ', 'print(', 'if ', 'for ', 'while ']):
                score += 20
            
            if score > best_score:
                best_score = score
                best_paragraph = paragraph
        
        if best_paragraph:
            # Clean up the paragraph
            cleaned = re.sub(r'\s+', ' ', best_paragraph.strip())
            if len(cleaned) > max_length:
                cleaned = cleaned[:max_length] + "..."
            return cleaned
        
        # Fallback: return first meaningful content with code
        lines = content.split('\n')
        meaningful_lines = []
        code_found = False
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('===') and not line.startswith('Title:'):
                meaningful_lines.append(line)
                
                # Check if we found code
                if any(code_indicator in line for code_indicator in ['def ', 'class ', 'import ', 'print(', 'if ', 'for ', 'while ']):
                    code_found = True
                
                if len('\n'.join(meaningful_lines)) > max_length:
                    break
        
        result = '\n'.join(meaningful_lines)
        if len(result) > max_length:
            result = result[:max_length] + "..."
        
        if code_found:
            result += "\n\n💻 This chapter contains code examples!"
        
        return result
    
    def query(self, question: str) -> str:
        """Query the simple RAG system with detailed responses"""
        if not self.is_initialized:
            return "RAG system not initialized. Please try again."
        
        try:
            logger.info(f"Processing question: {question[:50]}...")
            
            # Search for relevant chapters
            results = self.search_chapters(question, top_k=5)  # Get more results
            
            if not results:
                return "I couldn't find relevant information about that in the Python Crash Course book."
            
            # Create a detailed response
            response = f"Based on the Python Crash Course book, here's what I found:\n\n"
            response += f"📖 Main Chapter: {results[0]['title']}\n\n"
            
            # Get the best snippet from the main chapter
            best_match = results[0]
            chapter_content = best_match['chapter']['content']
            snippet = self.find_best_snippet(chapter_content, question)
            
            # Check if this is a code-related question
            code_keywords = ['function', 'def', 'class', 'code', 'example', 'syntax', 'program', 'method', 'loop', 'variable']
            is_code_question = any(keyword in question.lower() for keyword in code_keywords)
            
            if is_code_question:
                response += f"💻 Complete Code Example:\n{snippet}\n\n"
            else:
                response += f"📝 Detailed Explanation:\n{snippet}\n\n"
            
            response += f"💡 This information comes from the Python Crash Course book by Eric Matthes.\n\n"
            
            # Add additional examples from other chapters
            if len(results) > 1:
                response += f"🔍 Additional Examples from Other Chapters:\n"
                for i, result in enumerate(results[1:4], 2):  # Show up to 3 more
                    response += f"\n📖 Chapter {i}: {result['title']}\n"
                    # Get a shorter snippet from additional chapters
                    additional_snippet = self.find_best_snippet(result['chapter']['content'], question, max_length=300)
                    response += f"📝 {additional_snippet[:200]}...\n"
            
            # Add usage tips for code questions
            if is_code_question:
                response += f"\n💡 Usage Tips:\n"
                response += f"• Copy the code examples and run them in your Python environment\n"
                response += f"• Experiment with the code by modifying parameters\n"
                response += f"• Check the book for more detailed explanations\n"
            
            return response
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"Error processing your question: {str(e)}"

# Global RAG instance
simple_rag_system = SimpleBookRAG()

def initialize_simple_rag():
    """Initialize the simple RAG system"""
    return simple_rag_system.initialize()

def query_simple_rag(question: str) -> str:
    """Query the simple RAG system"""
    return simple_rag_system.query(question)

# Test function
def test_simple_rag():
    """Test the simple RAG system"""
    print("🚀 Testing Simple Book RAG System")
    print("=" * 50)
    
    if not initialize_simple_rag():
        print("❌ Failed to initialize RAG system")
        return
    
    test_queries = [
        "What is Python?",
        "How do I install Python?",
        "What are variables in Python?",
        "How do I create a function in Python?"
    ]
    
    print("\n🤖 Testing with sample queries:")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n❓ Query {i}: {query}")
        response = query_simple_rag(query)
        print(f"💡 Answer: {response}")
    
    print("\n🎉 Simple RAG system is ready!")

if __name__ == "__main__":
    test_simple_rag() 