import React from 'react';
import { ArrowLeft, CheckCircle, XCircle, AlertCircle, ExternalLink } from 'lucide-react';

export default function Results({ results, onReset }) {
  if (!results || results.length === 0) {
    return (
      <div className="bg-gh-card border border-gh-border p-8 rounded-md max-w-3xl w-full mx-auto text-center">
        <h2 className="text-xl font-bold text-gh-text mb-4">No Recommendations Found</h2>
        <p className="text-gh-muted text-sm mb-6">We couldn't find any products that match your hard requirements.</p>
        <button onClick={onReset} className="btn-secondary">Back to Questionnaire</button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl w-full mx-auto space-y-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gh-text">
          Results
        </h2>
        <button onClick={onReset} className="btn-secondary flex items-center gap-2">
          <ArrowLeft className="w-4 h-4" /> Start Over
        </button>
      </div>

      <div className="space-y-4">
        {results.map((item, idx) => {
          const { product, score, reasons } = item;
          const isTopMatch = idx === 0 && score > 0;
          
          return (
            <div key={product.id} className={`bg-gh-card border p-5 rounded-md relative ${isTopMatch ? 'border-gh-green' : 'border-gh-border'}`}>
              {isTopMatch && (
                <div className="absolute top-0 right-0 bg-gh-green text-white text-[10px] font-bold px-2 py-0.5 rounded-bl-sm uppercase tracking-wider">
                  Top Match
                </div>
              )}
              
              <div className="flex flex-col md:flex-row gap-6">
                {/* Score & Basic Info */}
                <div className="flex-shrink-0 md:w-40 flex flex-col items-center justify-center text-center border-b md:border-b-0 md:border-r border-gh-border pb-4 md:pb-0 md:pr-4">
                  <div className="text-4xl font-bold mb-2">
                    <span className={`${score > 75 ? 'text-gh-green' : score > 40 ? 'text-yellow-500' : 'text-red-500'}`}>
                      {score}
                    </span>
                    <span className="text-gh-muted text-lg">/100</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gh-text">{product.vendor}</h3>
                    <p className="text-gh-muted text-xs font-semibold">{product.model}</p>
                    <div className="mt-2 inline-block px-2 py-0.5 rounded-sm text-[10px] bg-gh-bg border border-gh-border text-gh-muted uppercase">
                      {product.category}
                    </div>
                  </div>
                </div>

                {/* Details */}
                <div className="flex-1 space-y-4">
                  <p className="text-gh-text text-sm leading-relaxed">{product.notes}</p>
                  
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-3 border-y border-gh-border">
                    <div>
                      <div className="text-[10px] text-gh-muted uppercase tracking-wider mb-1">Max Bandwidth</div>
                      <div className="text-sm font-semibold text-gh-text">{product.scale.max_bandwidth_Tbps} Tbps</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-gh-muted uppercase tracking-wider mb-1">400G Ports</div>
                      <div className="text-sm font-semibold text-gh-text">{product.interfaces['400G'] || 0}</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-gh-muted uppercase tracking-wider mb-1">OS</div>
                      <div className="text-sm font-semibold text-gh-text">{product.os}</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-gh-muted uppercase tracking-wider mb-1">Licensing</div>
                      <div className="text-sm font-semibold text-gh-text capitalize">{product.licensing.model}</div>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-xs font-bold text-gh-text mb-2 uppercase tracking-wide">Score Breakdown</h4>
                    <ul className="space-y-1.5">
                      {reasons.map((reason, i) => {
                        let Icon = AlertCircle;
                        let colorClass = "text-yellow-500";
                        if (reason.startsWith("✓")) {
                          Icon = CheckCircle;
                          colorClass = "text-gh-green";
                        } else if (reason.startsWith("✗")) {
                          Icon = XCircle;
                          colorClass = "text-red-500";
                        }
                        
                        return (
                          <li key={i} className="flex items-start text-xs text-gh-text">
                            <Icon className={`w-3.5 h-3.5 mr-2 mt-0.5 flex-shrink-0 ${colorClass}`} />
                            <span>{reason.substring(2)}</span>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                  
                  {(product.links?.datasheet || product.links?.product_page) && (
                    <div className="flex gap-4 pt-2">
                      {product.links.datasheet && (
                        <a href={product.links.datasheet} target="_blank" rel="noopener noreferrer" className="text-xs text-primary-400 hover:underline flex items-center gap-1">
                          Datasheet <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                      {product.links.product_page && (
                        <a href={product.links.product_page} target="_blank" rel="noopener noreferrer" className="text-xs text-primary-400 hover:underline flex items-center gap-1">
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
