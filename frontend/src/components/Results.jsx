import React from 'react';
import { ArrowLeft, CheckCircle, XCircle, AlertCircle, ExternalLink } from 'lucide-react';

export default function Results({ results, onReset }) {
  if (!results || results.length === 0) {
    return (
      <div className="glass p-8 rounded-2xl max-w-3xl w-full mx-auto text-center animate-in fade-in zoom-in duration-500">
        <h2 className="text-2xl font-bold text-slate-200 mb-4">No Recommendations Found</h2>
        <p className="text-slate-400 mb-6">We couldn't find any products that match your hard requirements.</p>
        <button onClick={onReset} className="btn-primary">Back to Questionnaire</button>
      </div>
    );
  }

  return (
    <div className="max-w-5xl w-full mx-auto animate-in fade-in slide-in-from-bottom-8 duration-500 space-y-6">
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-primary-600">
          Recommended Hardware
        </h2>
        <button onClick={onReset} className="btn-secondary flex items-center gap-2">
          <ArrowLeft className="w-4 h-4" /> Start Over
        </button>
      </div>

      <div className="space-y-6">
        {results.map((item, idx) => {
          const { product, score, reasons } = item;
          const isTopMatch = idx === 0 && score > 0;
          
          return (
            <div key={product.id} className={`glass p-6 rounded-2xl relative overflow-hidden transition-all duration-300 ${isTopMatch ? 'ring-2 ring-primary-500 shadow-xl shadow-primary-500/20' : ''}`}>
              {isTopMatch && (
                <div className="absolute top-0 right-0 bg-gradient-to-l from-primary-500 to-teal-400 text-white text-xs font-bold px-4 py-1 rounded-bl-lg">
                  Top Match
                </div>
              )}
              
              <div className="flex flex-col md:flex-row gap-6">
                {/* Score & Basic Info */}
                <div className="flex-shrink-0 md:w-48 flex flex-col items-center justify-center text-center border-b md:border-b-0 md:border-r border-slate-700/50 pb-6 md:pb-0 md:pr-6">
                  <div className="relative inline-flex items-center justify-center">
                    <svg className="w-24 h-24 transform -rotate-90">
                      <circle cx="48" cy="48" r="44" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-slate-700/50" />
                      <circle cx="48" cy="48" r="44" stroke="currentColor" strokeWidth="8" fill="transparent" strokeDasharray={`${(score / 100) * 276} 276`} className={`${score > 75 ? 'text-teal-500' : score > 40 ? 'text-yellow-500' : 'text-red-500'} transition-all duration-1000 ease-out`} />
                    </svg>
                    <span className="absolute text-2xl font-bold text-slate-100">{score}</span>
                  </div>
                  <div className="mt-4">
                    <h3 className="text-xl font-bold text-slate-100">{product.vendor}</h3>
                    <p className="text-slate-400 font-medium">{product.model}</p>
                    <div className="mt-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700">
                      {product.category}
                    </div>
                  </div>
                </div>

                {/* Details */}
                <div className="flex-1 space-y-4">
                  <p className="text-slate-300 text-sm leading-relaxed">{product.notes}</p>
                  
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-4 border-y border-slate-700/50">
                    <div>
                      <div className="text-xs text-slate-500 mb-1">Max Bandwidth</div>
                      <div className="font-semibold text-slate-200">{product.scale.max_bandwidth_Tbps} Tbps</div>
                    </div>
                    <div>
                      <div className="text-xs text-slate-500 mb-1">400G Ports</div>
                      <div className="font-semibold text-slate-200">{product.interfaces['400G'] || 0}</div>
                    </div>
                    <div>
                      <div className="text-xs text-slate-500 mb-1">OS</div>
                      <div className="font-semibold text-slate-200">{product.os}</div>
                    </div>
                    <div>
                      <div className="text-xs text-slate-500 mb-1">Licensing</div>
                      <div className="font-semibold text-slate-200 capitalize">{product.licensing.model}</div>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold text-slate-300 mb-2">Score Breakdown</h4>
                    <ul className="space-y-1">
                      {reasons.map((reason, i) => {
                        let Icon = AlertCircle;
                        let colorClass = "text-yellow-400";
                        if (reason.startsWith("✓")) {
                          Icon = CheckCircle;
                          colorClass = "text-teal-400";
                        } else if (reason.startsWith("✗")) {
                          Icon = XCircle;
                          colorClass = "text-red-400";
                        }
                        
                        return (
                          <li key={i} className="flex items-start text-sm text-slate-400">
                            <Icon className={`w-4 h-4 mr-2 mt-0.5 flex-shrink-0 ${colorClass}`} />
                            <span>{reason.substring(2)}</span>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                  
                  {(product.links?.datasheet || product.links?.product_page) && (
                    <div className="flex gap-4 pt-2">
                      {product.links.datasheet && (
                        <a href={product.links.datasheet} target="_blank" rel="noopener noreferrer" className="text-sm text-primary-400 hover:text-primary-300 flex items-center gap-1 transition-colors">
                          Datasheet <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                      {product.links.product_page && (
                        <a href={product.links.product_page} target="_blank" rel="noopener noreferrer" className="text-sm text-primary-400 hover:text-primary-300 flex items-center gap-1 transition-colors">
                          Product Page <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
