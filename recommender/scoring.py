"""
Scoring module for the Network Hardware Recommendation Engine.
"""
from typing import List, Tuple
from pydantic import BaseModel

from recommender.models import Product, Questionnaire

class ScoredProduct(BaseModel):
    product: Product
    score: int
    reasons: List[str]

# Configurable scoring weights
WEIGHTS = {
    "capacity_match": 20,
    "routing_scale_match": 20,
    "feature_match": 20,
    "subscriber_scale_match": 15,
    "licensing_preference_match": 10,
    "os_preference_match": 15
}

def evaluate_product(q: Questionnaire, p: Product) -> Tuple[int, List[str], bool]:
    """Evaluate a single product and return its score, reasoning, and whether it's disqualified."""
    reasons = []
    score = 0
    disqualified = False
    
    # 1. Hard Disqualifiers
    
    # Routing Scale Disqualifiers
    if q.full_bgp_table and not p.capabilities.full_bgp_table:
        reasons.append("✗ Does not support full BGP table")
        disqualified = True
        
    if p.capabilities.max_bgp_peers < q.min_bgp_peers:
        reasons.append(f"✗ Supports only {p.capabilities.max_bgp_peers} BGP peers (need {q.min_bgp_peers})")
        disqualified = True
        
    if p.capabilities.max_vrfs < q.min_vrfs:
        reasons.append(f"✗ Supports only {p.capabilities.max_vrfs} VRFs (need {q.min_vrfs})")
        disqualified = True
        
    if p.capabilities.max_ipv4_routes < q.min_ipv4_routes:
        reasons.append(f"✗ Supports only {p.capabilities.max_ipv4_routes} IPv4 routes (need {q.min_ipv4_routes})")
        disqualified = True
        
    # Capacity Disqualifiers
    if p.capabilities.max_backhaul_G < q.required_backhaul_G:
        reasons.append(f"✗ Max backhaul speed is {p.capabilities.max_backhaul_G}G (need {q.required_backhaul_G}G)")
        disqualified = True
        
    if p.interfaces.speed_400G < q.min_400G:
        reasons.append(f"✗ Has only {p.interfaces.speed_400G} 400G ports (need {q.min_400G})")
        disqualified = True
        
    if p.interfaces.speed_100G < q.min_100G:
        reasons.append(f"✗ Has only {p.interfaces.speed_100G} 100G ports (need {q.min_100G})")
        disqualified = True
        
    if p.scale.max_bandwidth_Tbps < q.peak_bandwidth_Tbps:
        reasons.append(f"✗ Bandwidth capacity {p.scale.max_bandwidth_Tbps}Tbps is less than peak {q.peak_bandwidth_Tbps}Tbps")
        disqualified = True
        
    # Feature Disqualifiers
    if q.needs_mpls and not p.capabilities.mpls:
        reasons.append("✗ Missing MPLS support")
        disqualified = True
        
    if q.needs_segment_routing and not p.capabilities.segment_routing:
        reasons.append("✗ Missing Segment Routing support")
        disqualified = True
        
    if q.needs_bng and not p.capabilities.bng:
        reasons.append("✗ Missing BNG support")
        disqualified = True
        
    if disqualified:
        return 0, reasons, True
        
    # 2. Soft Scoring
    
    # Capacity matching
    score += WEIGHTS["capacity_match"]
    reasons.append(f"✓ Meets capacity requirements ({p.scale.max_bandwidth_Tbps}Tbps)")
    
    # Routing Scale matching
    score += WEIGHTS["routing_scale_match"]
    reasons.append(f"✓ Meets routing scale requirements ({p.capabilities.max_ipv4_routes} routes, {p.capabilities.max_vrfs} VRFs)")
    
    # Feature matching
    feature_score = 0
    features_needed = 0
    features_met = 0
    
    for q_attr, p_attr, feature_name in [
        ("needs_evpn", "evpn", "EVPN"),
        ("needs_ptp", "ptp", "PTP"),
        ("needs_macsec", "macsec", "MACsec"),
        ("needs_openconfig", "openconfig", "OpenConfig"),
        ("needs_streaming_telemetry", "streaming_telemetry", "Streaming Telemetry")
    ]:
        if getattr(q, q_attr):
            features_needed += 1
            if getattr(p.capabilities, p_attr):
                features_met += 1
                reasons.append(f"✓ Supports {feature_name}")
            else:
                reasons.append(f"~ Missing optional {feature_name} support")
                
    if features_needed == 0:
        score += WEIGHTS["feature_match"]
    else:
        score += int(WEIGHTS["feature_match"] * (features_met / features_needed))
        
    # Subscriber scale match
    if q.needs_bng and q.subscribers_5yr is not None and p.scale.subscriber_scale is not None:
        if p.scale.subscriber_scale >= q.subscribers_5yr:
            score += WEIGHTS["subscriber_scale_match"]
            reasons.append(f"✓ Meets 5-year subscriber growth ({p.scale.subscriber_scale:,} > {q.subscribers_5yr:,})")
        else:
            reasons.append(f"~ Subscriber scale {p.scale.subscriber_scale:,} is tight for your 5-year projection of {q.subscribers_5yr:,}")
    else:
        score += WEIGHTS["subscriber_scale_match"]
        
    # Operational Preference
    if q.preferred_os and q.preferred_os.lower() in p.os.lower():
        score += WEIGHTS["os_preference_match"]
        reasons.append(f"✓ Matches preferred OS ecosystem ({p.os})")
    elif q.preferred_os:
        reasons.append(f"~ Different OS ecosystem ({p.os} vs requested {q.preferred_os})")
    else:
        score += WEIGHTS["os_preference_match"]
        
    # Licensing Preference
    if q.preferred_licensing != "no-preference":
        if p.licensing.model == q.preferred_licensing:
            score += WEIGHTS["licensing_preference_match"]
            reasons.append(f"✓ Matches preferred licensing model ({p.licensing.model})")
        else:
            reasons.append(f"~ Different licensing model ({p.licensing.model} vs requested {q.preferred_licensing})")
    else:
        score += WEIGHTS["licensing_preference_match"]
        
    # Cap score at 100
    score = min(100, score)
    
    return score, reasons, False


def score_products(questionnaire: Questionnaire, products: List[Product]) -> List[ScoredProduct]:
    """Score a list of products against the questionnaire."""
    scored = []
    
    for product in products:
        score, reasons, disqualified = evaluate_product(questionnaire, product)
        if not disqualified:
            scored.append(ScoredProduct(product=product, score=score, reasons=reasons))
            
    # Sort by score descending, tie-break by prioritizing perpetual licensing
    scored.sort(key=lambda x: (x.score, x.product.licensing.model == "perpetual"), reverse=True)
    return scored
