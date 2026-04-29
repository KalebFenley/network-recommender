import React, { useState } from 'react';
import Questionnaire from './components/Questionnaire';
import Results from './components/Results';
import { Terminal } from 'lucide-react';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendations = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Failed to fetch recommendations');
      }
      
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gh-bg text-gh-text font-mono pb-20">
      <header className="border-b border-gh-border bg-gh-bg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Terminal className="w-5 h-5 text-gh-text" />
            <h1 className="text-lg font-semibold tracking-tight">NetRec Engine</h1>
          </div>
          <nav className="text-xs text-gh-muted">
            v1.0.0-rc
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 pt-12">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight mb-4 text-gh-text">
            Find the right gear.
          </h2>
          <p className="text-sm text-gh-muted max-w-2xl mx-auto">
            Provide your network requirements below. The engine will score and rank hardware options based on capacity, scale, and feature support.
          </p>
        </div>

        {error && (
          <div className="max-w-3xl mx-auto mb-6 p-4 border border-red-900 bg-[#3a1d1d] text-red-400 rounded-md flex items-center justify-center text-sm">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 space-y-4">
            <div className="w-8 h-8 border-2 border-gh-border border-t-gh-text rounded-full animate-spin" />
            <p className="text-gh-muted text-sm animate-pulse">Running scoring matrix...</p>
          </div>
        ) : results ? (
          <Results results={results} onReset={handleReset} />
        ) : (
          <Questionnaire onSubmit={fetchRecommendations} />
        )}
      </main>
    </div>
  );
}

export default App;
