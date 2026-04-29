"""
Tests for the Pydantic models.
"""
import pytest
from pydantic import ValidationError
from recommender.models import Product, Questionnaire

def test_product_model_valid():
    data = {
        "id": "test-router",
        "vendor": "Test Vendor",
        "product_line": "Test Line",
        "model": "Test Model",
        "category": "core-router",
        "interfaces": {
            "400G": 32,
            "100G": 0,
            "40G": 0,
            "10G": 0,
            "1G": 0
        },
        "capabilities": {
            "max_backhaul_G": 400,
            "full_bgp_table": True,
            "max_bgp_peers": 4000,
            "max_vrfs": 4000,
            "max_ipv4_routes": 4000000,
            "mpls": True,
            "segment_routing": True,
            "evpn": True,
            "bng": False,
            "ptp": True,
            "macsec": True,
            "openconfig": True,
            "streaming_telemetry": True
        },
        "scale": {
            "max_bandwidth_Tbps": 12.8,
            "subscriber_scale": None
        },
        "os": "Test OS",
        "licensing": {
            "model": "subscription",
            "notes": "Test notes"
        },
        "notes": "General notes",
        "links": {
            "datasheet": "https://example.com/datasheet",
            "product_page": "https://example.com/product"
        }
    }
    
    product = Product.model_validate(data)
    assert product.id == "test-router"
    assert product.interfaces.speed_400G == 32
    assert str(product.links.datasheet) == "https://example.com/datasheet"

def test_product_model_invalid_category():
    data = {
        "id": "test",
        "vendor": "V",
        "product_line": "L",
        "model": "M",
        "category": "invalid-category",
        "interfaces": {"400G": 1},
        "capabilities": {
            "max_backhaul_G": 1, "full_bgp_table": False, "max_bgp_peers": 1,
            "max_vrfs": 1, "max_ipv4_routes": 1, "mpls": False, "segment_routing": False,
            "evpn": False, "bng": False, "ptp": False, "macsec": False,
            "openconfig": False, "streaming_telemetry": False
        },
        "scale": {"max_bandwidth_Tbps": 1.0},
        "os": "O",
        "licensing": {"model": "perpetual", "notes": ""},
        "notes": "",
        "links": {}
    }
    
    with pytest.raises(ValidationError):
        Product.model_validate(data)

def test_questionnaire_model_defaults():
    data = {
        "required_backhaul_G": 100,
        "full_bgp_table": False,
        "min_bgp_peers": 10,
        "min_vrfs": 0,
        "min_ipv4_routes": 1000,
        "peak_bandwidth_Tbps": 0.5,
        "role": "edge-router",
        "needs_mpls": False,
        "needs_segment_routing": False,
        "needs_bng": False,
        "needs_evpn": False,
        "needs_ptp": False,
        "needs_macsec": False,
        "needs_openconfig": False,
        "needs_streaming_telemetry": False
    }
    
    q = Questionnaire.model_validate(data)
    assert q.min_400G == 0
    assert q.preferred_licensing == "no-preference"
