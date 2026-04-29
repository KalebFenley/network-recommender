import React, { useState } from 'react';
import { ArrowRight, ArrowLeft, TerminalSquare } from 'lucide-react';

const STEPS = [
  { id: 'capacity', title: 'Capacity & Interfaces' },
  { id: 'routing', title: 'Routing Scale' },
  { id: 'features', title: 'Features & Roles' },
  { id: 'prefs', title: 'Preferences' },
];

export default function Questionnaire({ onSubmit }) {
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({
    required_backhaul_G: 100,
    min_400G: 0,
    min_100G: 0,
    min_40G: 0,
    min_10G: 0,
    min_1G: 0,
    full_bgp_table: false,
    min_bgp_peers: 10,
    min_vrfs: 10,
    min_ipv4_routes: 10000,
    peak_bandwidth_value: 0.1,
    peak_bandwidth_unit: 'Tbps',
    role: 'core-router',
    needs_mpls: false,
    needs_segment_routing: false,
    needs_bng: false,
    subscribers_5yr: 0,
    needs_evpn: false,
    needs_ptp: false,
    needs_macsec: false,
    needs_openconfig: false,
    needs_streaming_telemetry: false,
    preferred_os: '',
    preferred_licensing: 'no-preference'
  });

  const updateForm = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => setStep(s => Math.min(s + 1, STEPS.length - 1));
  const handlePrev = () => setStep(s => Math.max(s - 1, 0));
  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = { ...formData };
    payload.subscribers_5yr = payload.subscribers_5yr ? parseInt(payload.subscribers_5yr) : null;
    
    payload.peak_bandwidth_Tbps = payload.peak_bandwidth_unit === 'Gbps' 
      ? parseFloat(payload.peak_bandwidth_value) / 1000 
      : parseFloat(payload.peak_bandwidth_value);
      
    delete payload.peak_bandwidth_value;
    delete payload.peak_bandwidth_unit;

    onSubmit(payload);
  };

  return (
    <div className="bg-gh-card border border-gh-border p-8 rounded-md max-w-3xl w-full mx-auto">
      <div className="mb-8">
        <h2 className="text-xl font-bold text-gh-text mb-3">
          {STEPS[step].title}
        </h2>
        <div className="flex gap-1">
          {STEPS.map((s, i) => (
            <div key={s.id} className={`h-1.5 flex-1 rounded-sm transition-colors duration-300 ${i <= step ? 'bg-gh-green' : 'bg-gh-border'}`} />
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {step === 0 && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gh-text mb-1">Max Backhaul Speed (G)</label>
              <select className="input-field w-full" value={formData.required_backhaul_G} onChange={(e) => updateForm('required_backhaul_G', parseInt(e.target.value))}>
                <option value={1}>1G</option>
                <option value={10}>10G</option>
                <option value={40}>40G</option>
                <option value={100}>100G</option>
                <option value={400}>400G</option>
                <option value={800}>800G</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gh-text mb-1">Peak Bandwidth</label>
              <div className="flex gap-2">
                <input type="number" step="any" className="input-field w-full" value={formData.peak_bandwidth_value} onChange={(e) => updateForm('peak_bandwidth_value', e.target.value)} />
                <select className="input-field w-24 shrink-0" value={formData.peak_bandwidth_unit} onChange={(e) => updateForm('peak_bandwidth_unit', e.target.value)}>
                  <option value="Tbps">Tbps</option>
                  <option value="Gbps">Gbps</option>
                </select>
              </div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs text-gh-muted mb-1">Min 400G Ports</label>
                <input type="number" min="0" className="input-field w-full" value={formData.min_400G} onChange={(e) => updateForm('min_400G', parseInt(e.target.value) || 0)} />
              </div>
              <div>
                <label className="block text-xs text-gh-muted mb-1">Min 100G Ports</label>
                <input type="number" min="0" className="input-field w-full" value={formData.min_100G} onChange={(e) => updateForm('min_100G', parseInt(e.target.value) || 0)} />
              </div>
              <div>
                <label className="block text-xs text-gh-muted mb-1">Min 10G Ports</label>
                <input type="number" min="0" className="input-field w-full" value={formData.min_10G} onChange={(e) => updateForm('min_10G', parseInt(e.target.value) || 0)} />
              </div>
            </div>
          </div>
        )}

        {step === 1 && (
          <div className="space-y-4">
            <label className="flex items-center space-x-3 p-4 bg-gh-bg border border-gh-border rounded-md cursor-pointer hover:border-gh-muted transition-colors">
              <input type="checkbox" className="form-checkbox h-4 w-4 text-primary-500 rounded border-gh-border bg-gh-bg" checked={formData.full_bgp_table} onChange={(e) => updateForm('full_bgp_table', e.target.checked)} />
              <span className="text-gh-text text-sm">Requires Full BGP Table Support</span>
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gh-text mb-1">Min BGP Peers</label>
                <input type="number" min="0" className="input-field w-full" value={formData.min_bgp_peers} onChange={(e) => updateForm('min_bgp_peers', parseInt(e.target.value) || 0)} />
              </div>
              <div>
                <label className="block text-sm font-medium text-gh-text mb-1">Min VRFs</label>
                <input type="number" min="0" className="input-field w-full" value={formData.min_vrfs} onChange={(e) => updateForm('min_vrfs', parseInt(e.target.value) || 0)} />
              </div>
              <div>
                <label className="block text-sm font-medium text-gh-text mb-1">Min IPv4 Routes</label>
                <input type="number" min="0" className="input-field w-full" value={formData.min_ipv4_routes} onChange={(e) => updateForm('min_ipv4_routes', parseInt(e.target.value) || 0)} />
              </div>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gh-text mb-1">Network Role</label>
              <select className="input-field w-full" value={formData.role} onChange={(e) => updateForm('role', e.target.value)}>
                <option value="core-router">Core Router</option>
                <option value="edge-router">Edge Router</option>
                <option value="peering-router">Peering Router</option>
                <option value="aggregation">Aggregation</option>
                <option value="access">Access</option>
              </select>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {[
                { id: 'needs_mpls', label: 'MPLS' },
                { id: 'needs_segment_routing', label: 'Segment Routing' },
                { id: 'needs_evpn', label: 'EVPN' },
                { id: 'needs_bng', label: 'BNG / PPPoE' },
                { id: 'needs_ptp', label: 'PTP Timing' },
                { id: 'needs_macsec', label: 'MACsec' },
                { id: 'needs_openconfig', label: 'OpenConfig' },
                { id: 'needs_streaming_telemetry', label: 'Streaming Telemetry' }
              ].map(feat => (
                <label key={feat.id} className="flex items-center space-x-3 p-3 bg-gh-bg border border-gh-border rounded-md cursor-pointer hover:border-gh-muted transition-colors">
                  <input type="checkbox" className="form-checkbox h-3.5 w-3.5 text-primary-500 rounded border-gh-border bg-gh-bg" checked={formData[feat.id]} onChange={(e) => updateForm(feat.id, e.target.checked)} />
                  <span className="text-gh-text text-xs">{feat.label}</span>
                </label>
              ))}
            </div>
            {formData.needs_bng && (
              <div>
                <label className="block text-sm font-medium text-gh-text mb-1">Expected Subscribers (5yr)</label>
                <input type="number" min="0" className="input-field w-full" value={formData.subscribers_5yr} onChange={(e) => updateForm('subscribers_5yr', e.target.value)} />
              </div>
            )}
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gh-text mb-1">Preferred Licensing Model</label>
              <select className="input-field w-full" value={formData.preferred_licensing} onChange={(e) => updateForm('preferred_licensing', e.target.value)}>
                <option value="no-preference">No Preference</option>
                <option value="perpetual">Perpetual</option>
                <option value="subscription">Subscription</option>
                <option value="mixed">Mixed</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gh-text mb-1">Preferred OS Ecosystem (Optional)</label>
              <input type="text" placeholder="e.g. IOS-XR, JunOS, EOS" className="input-field w-full" value={formData.preferred_os} onChange={(e) => updateForm('preferred_os', e.target.value)} />
            </div>
          </div>
        )}

        <div className="flex justify-between pt-6 mt-6 border-t border-gh-border">
          <button type="button" onClick={handlePrev} disabled={step === 0} className={`btn-secondary flex items-center gap-2 ${step === 0 ? 'opacity-50 cursor-not-allowed' : ''}`}>
            <ArrowLeft className="w-4 h-4" /> Back
          </button>
          
          {step < STEPS.length - 1 ? (
            <button type="button" onClick={handleNext} className="btn-secondary flex items-center gap-2">
              Next <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button type="submit" className="btn-primary flex items-center gap-2">
              Run Matrix <TerminalSquare className="w-4 h-4" />
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
