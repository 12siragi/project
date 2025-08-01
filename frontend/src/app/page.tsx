'use client';

import { useState, useEffect } from 'react';

interface Question {
  id: string;
  question: string;
  answer: string;
  timestamp: Date;
  source: string;
}

export default function Home() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [recentQuestions, setRecentQuestions] = useState<Question[]>([]);
  const [error, setError] = useState('');
  const [useRAG, setUseRAG] = useState(false);

  // Load recent questions from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('askAfrica_recent_questions');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setRecentQuestions(parsed.map((q: any) => ({
          ...q,
          timestamp: new Date(q.timestamp)
        })));
      } catch (e) {
        console.error('Error loading recent questions:', e);
      }
    }
  }, []);

  const saveRecentQuestion = (question: string, answer: string, source: string) => {
    const newQuestion: Question = {
      id: Date.now().toString(),
      question,
      answer,
      timestamp: new Date(),
      source
    };

    const updated = [newQuestion, ...recentQuestions.slice(0, 9)]; // Keep last 10
    setRecentQuestions(updated);
    localStorage.setItem('askAfrica_recent_questions', JSON.stringify(updated));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsLoading(true);
    setError('');
    setAnswer('');

    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question.trim(),
          use_rag: useRAG
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAnswer(data.answer);
      saveRecentQuestion(question.trim(), data.answer, data.source);
      setQuestion('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (timestamp: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(timestamp);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AskAfrica
          </h1>
          <p className="text-lg text-gray-600">
            Your local AI assistant powered by Ollama
          </p>
        </div>

        {/* Main Q&A Interface */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* RAG Toggle */}
            <div className="flex items-center justify-center space-x-4">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={useRAG}
                  onChange={(e) => setUseRAG(e.target.checked)}
                  className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
                />
                <span className="text-sm font-medium text-gray-700">
                  📚 Search Python Crash Course Book
                </span>
              </label>
            </div>

            <div>
              <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
                {useRAG ? "Ask about Python Crash Course..." : "Ask anything..."}
              </label>
              <textarea
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder={useRAG ? "What would you like to know about Python?" : "What would you like to know?"}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg text-black focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                rows={3}
                disabled={isLoading}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !question.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Thinking...</span>
                </>
              ) : (
                <>
                  <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span>{useRAG ? "Search Book" : "Ask AI"}</span>
                </>
              )}
            </button>
          </form>

          {/* Error Display */}
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {/* Answer Display */}
          {answer && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-medium text-green-800">AI Response:</h3>
                <span className="text-xs text-green-600 bg-green-100 px-2 py-1 rounded">
                  {useRAG ? "📚 Book Search" : "🤖 General AI"}
                </span>
              </div>
              <p className="text-green-700 whitespace-pre-wrap">{answer}</p>
            </div>
          )}
        </div>

        {/* Recent Questions */}
        {recentQuestions.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Recent Questions
            </h2>
            <div className="space-y-4">
              {recentQuestions.map((q) => (
                <div key={q.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-medium text-gray-900">{q.question}</h3>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-gray-500">{formatTime(q.timestamp)}</span>
                      <span className={`text-xs px-2 py-1 rounded ${
                        q.source === 'book_rag' 
                          ? 'bg-blue-100 text-blue-600' 
                          : 'bg-gray-100 text-gray-600'
                      }`}>
                        {q.source === 'book_rag' ? '📚 Book' : '🤖 AI'}
                      </span>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm line-clamp-2">{q.answer}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
