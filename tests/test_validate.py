"""
Tests for the validation script.
"""
import pytest
import yaml
from pathlib import Path
from recommender.validate import validate_all_products

def test_validate_all_products_empty(tmp_path, capsys):
    assert validate_all_products(tmp_path) is True
    captured = capsys.readouterr()
    assert "No product files found to validate." in captured.out
    
def test_validate_all_products_invalid_dir(capsys):
    assert validate_all_products(Path("/invalid/path")) is False
    captured = capsys.readouterr()
    assert "Directory not found:" in captured.out

def test_validate_all_products_success(tmp_path, capsys):
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
            "evpn": False, "bng": False, "ptp": False, "macsec": False, "nat": False,
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
        
    # Also create a template file to ensure it's skipped
    template_path = tmp_path / "_template.yaml"
    with open(template_path, "w") as f:
        yaml.dump({"id": "template"}, f)
        
    assert validate_all_products(tmp_path) is True
    captured = capsys.readouterr()
    assert "[OK] test.yaml is valid." in captured.out

def test_validate_all_products_invalid(tmp_path, capsys):
    product_data = {
        "id": "test-router",
        "category": "invalid",
        # Missing required fields
    }
    
    file_path = tmp_path / "test.yaml"
    with open(file_path, "w") as f:
        yaml.dump(product_data, f)
        
    assert validate_all_products(tmp_path) is False
    captured = capsys.readouterr()
    assert "[ERROR] Validation failed for" in captured.out
    
def test_validate_all_products_bad_yaml(tmp_path, capsys):
    file_path = tmp_path / "test.yaml"
    with open(file_path, "w") as f:
        f.write("invalid: yaml: :")
        
    assert validate_all_products(tmp_path) is False
    captured = capsys.readouterr()
    assert "[ERROR] Could not read test.yaml" in captured.out
