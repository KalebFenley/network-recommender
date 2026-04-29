"""
Tests for the database loader.
"""
import pytest
import yaml
from pathlib import Path
from recommender.database import load_products
from recommender.models import Product

def test_load_products_empty_dir(tmp_path):
    products = load_products(tmp_path)
    assert len(products) == 0

def test_load_products_invalid_dir():
    products = load_products(Path("/invalid/path/that/does/not/exist"))
    assert len(products) == 0

def test_load_products_success(tmp_path):
    product_data = {
        "id": "test-router",
        "vendor": "Test",
        "product_line": "Line",
        "model": "Model",
        "category": "core-router",
        "interfaces": {"400G": 32},
        "capabilities": {
            "max_backhaul_G": 400, "full_bgp_table": True, "max_bgp_peers": 1,
            "max_vrfs": 1, "max_ipv4_routes": 1, "mpls": False, "segment_routing": False,
            "evpn": False, "bng": False, "ptp": False, "macsec": False,
            "openconfig": False, "streaming_telemetry": False
        },
        "scale": {"max_bandwidth_Tbps": 12.8},
        "os": "Test OS",
        "licensing": {"model": "perpetual", "notes": ""},
        "notes": "",
        "links": {}
    }
    
    file_path = tmp_path / "test.yaml"
    with open(file_path, "w") as f:
        yaml.dump(product_data, f)
        
    template_path = tmp_path / "_template.yaml"
    with open(template_path, "w") as f:
        yaml.dump({"id": "template"}, f)
        
    products = load_products(tmp_path)
    assert len(products) == 1
    assert products[0].id == "test-router"

def test_load_products_invalid_yaml(tmp_path):
    file_path = tmp_path / "test.yaml"
    with open(file_path, "w") as f:
        f.write("invalid: yaml: :")
        
    with pytest.raises(ValueError, match="Failed to load product from"):
        load_products(tmp_path)
