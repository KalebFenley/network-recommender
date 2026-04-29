import React, { useState } from 'react';
import Questionnaire from './components/Questionnaire';
import Results from './components/Results';
import { Activity } from 'lucide-react';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendations = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/recommend', {
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
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans selection:bg-primary-500 selection:text-white pb-20 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary-900/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-teal-900/20 blur-[120px] pointer-events-none" />

      <header className="border-b border-slate-800/80 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-6 h-6 text-primary-500" />
            <h1 className="text-xl font-bold tracking-tight">NetRec</h1>
          </div>
          <nav className="text-sm text-slate-400">
            Hardware Recommendation Engine
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 pt-12 relative z-10">
        <div className="text-center mb-12 animate-in fade-in slide-in-from-top-4 duration-700">
          <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-br from-white to-slate-400">
            Find the right gear. <br className="hidden md:block" /> Without the vendor bias.
          </h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Answer a few questions about your network requirements and our engine will score and rank the best hardware options.
          </p>
        </div>

        {error && (
          <div className="max-w-3xl mx-auto mb-6 p-4 glass border-red-900/50 bg-red-900/10 text-red-400 rounded-xl flex items-center justify-center">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 space-y-4">
            <div className="w-12 h-12 border-4 border-slate-700 border-t-primary-500 rounded-full animate-spin" />
            <p className="text-slate-400 animate-pulse">Analyzing capabilities...</p>
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
