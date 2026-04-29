"""
Tests for the scoring module.
"""
from recommender.models import Product, Questionnaire
from recommender.scoring import evaluate_product, score_products, ScoredProduct

def create_product(**kwargs):
    default_data = {
        "id": "test",
        "vendor": "Test",
        "product_line": "Line",
        "model": "Model",
        "category": "core-router",
        "interfaces": {"400G": 0, "100G": 0, "40G": 0, "10G": 0, "1G": 0},
        "capabilities": {
            "max_backhaul_G": 0, "full_bgp_table": False, "max_bgp_peers": 0,
            "max_vrfs": 0, "max_ipv4_routes": 0, "mpls": False, "segment_routing": False,
            "evpn": False, "bng": False, "ptp": False, "macsec": False,
            "openconfig": False, "streaming_telemetry": False
        },
        "scale": {"max_bandwidth_Tbps": 0.0},
        "os": "TestOS",
        "licensing": {"model": "perpetual", "notes": ""},
        "notes": "",
        "links": {}
    }
    for key, value in kwargs.items():
        if isinstance(value, dict) and key in default_data:
            default_data[key].update(value)
        else:
            default_data[key] = value
            
    return Product.model_validate(default_data)

def create_questionnaire(**kwargs):
    default_data = {
        "required_backhaul_G": 0,
        "full_bgp_table": False,
        "min_bgp_peers": 0,
        "min_vrfs": 0,
        "min_ipv4_routes": 0,
        "peak_bandwidth_Tbps": 0.0,
        "role": "core-router",
        "needs_mpls": False,
        "needs_segment_routing": False,
        "needs_bng": False,
        "needs_evpn": False,
        "needs_ptp": False,
        "needs_macsec": False,
        "needs_openconfig": False,
        "needs_streaming_telemetry": False
    }
    default_data.update(kwargs)
    return Questionnaire.model_validate(default_data)

def test_evaluate_product_perfect_match():
    q = create_questionnaire(
        required_backhaul_G=400, full_bgp_table=True, min_bgp_peers=1000,
        min_vrfs=100, min_ipv4_routes=1000000, peak_bandwidth_Tbps=1.0,
        needs_mpls=True, needs_evpn=True, preferred_os="TestOS", preferred_licensing="perpetual",
        needs_bng=True, subscribers_5yr=1000
    )
    p = create_product(
        capabilities={"max_backhaul_G": 400, "full_bgp_table": True, "max_bgp_peers": 1000,
                      "max_vrfs": 100, "max_ipv4_routes": 1000000, "mpls": True, "evpn": True, "bng": True},
        scale={"max_bandwidth_Tbps": 1.0, "subscriber_scale": 1000}
    )
    
    score, reasons, dq = evaluate_product(q, p)
    assert dq is False
    assert score == 100

def test_evaluate_product_disqualified():
    # Test a few disqualifiers
    q = create_questionnaire(full_bgp_table=True, min_bgp_peers=1000, min_400G=2)
    p = create_product()
    score, reasons, dq = evaluate_product(q, p)
    assert dq is True
    assert any("✗ Does not support full BGP table" in r for r in reasons)
    assert any("✗ Supports only 0 BGP peers" in r for r in reasons)
    assert any("✗ Has only 0 400G ports" in r for r in reasons)

def test_evaluate_product_soft_scoring_os_licensing_mismatch():
    q = create_questionnaire(preferred_os="OtherOS", preferred_licensing="subscription")
    p = create_product(licensing={"model": "perpetual", "notes": ""})
    score, reasons, dq = evaluate_product(q, p)
    assert dq is False
    assert score < 100
    assert any("~ Different OS ecosystem" in r for r in reasons)
    assert any("~ Different licensing model" in r for r in reasons)

def test_evaluate_product_soft_scoring_features_mismatch():
    q = create_questionnaire(needs_evpn=True, needs_ptp=True)
    p = create_product(capabilities={"evpn": True}) # missing ptp
    score, reasons, dq = evaluate_product(q, p)
    assert dq is False
    assert any("✓ Supports EVPN" in r for r in reasons)
    assert any("~ Missing optional PTP support" in r for r in reasons)

def test_evaluate_product_subscriber_tight():
    q = create_questionnaire(needs_bng=True, subscribers_5yr=1000)
    p = create_product(capabilities={"bng": True}, scale={"subscriber_scale": 500})
    score, reasons, dq = evaluate_product(q, p)
    assert dq is False
    assert any("~ Subscriber scale" in r for r in reasons)

def test_score_products():
    q = create_questionnaire()
    q.preferred_os = "TestOS"
    
    p1 = create_product(id="p1")
    p2 = create_product(id="p2", os="OtherOS")
    p3 = create_product(id="p3", capabilities={"max_backhaul_G": -1}) # To be disqualified
    q.required_backhaul_G = 0
    
    scored = score_products(q, [p1, p2, p3])
    assert len(scored) == 2
    assert scored[0].product.id == "p1"
    assert scored[0].score > scored[1].score

def test_evaluate_product_disqualified_vrfs():
    q = create_questionnaire(min_vrfs=10)
    p = create_product()
    score, reasons, dq = evaluate_product(q, p)
    assert dq is True
    assert any("✗ Supports only" in r and "VRFs" in r for r in reasons)

def test_evaluate_product_disqualified_ipv4():
    q = create_questionnaire(min_ipv4_routes=1000)
    p = create_product()
    score, reasons, dq = evaluate_product(q, p)
    assert dq is True
    assert any("IPv4 routes" in r for r in reasons)

def test_evaluate_product_disqualified_100G():
    q = create_questionnaire(min_100G=2)
    p = create_product()
    score, reasons, dq = evaluate_product(q, p)
    assert dq is True
    assert any("100G ports" in r for r in reasons)

def test_evaluate_product_disqualified_bandwidth():
    q = create_questionnaire(peak_bandwidth_Tbps=10.0)
    p = create_product()
    score, reasons, dq = evaluate_product(q, p)
    assert dq is True
    assert any("Bandwidth capacity" in r for r in reasons)

def test_evaluate_product_disqualified_mpls():
    q = create_questionnaire(needs_mpls=True)
    p = create_product()
    score, reasons, dq = evaluate_product(q, p)
    assert dq is True
    assert any("Missing MPLS support" in r for r in reasons)

def test_evaluate_product_disqualified_sr():
    q = create_questionnaire(needs_segment_routing=True)
    p = create_product()
    score, reasons, dq = evaluate_product(q, p)
    assert dq is True
    assert any("Missing Segment Routing support" in r for r in reasons)

def test_evaluate_product_disqualified_bng():
    q = create_questionnaire(needs_bng=True)
    p = create_product()
    score, reasons, dq = evaluate_product(q, p)
    assert dq is True
    assert any("Missing BNG support" in r for r in reasons)

