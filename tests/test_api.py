"""
Tests for the FastAPI application.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from recommender.main import app, startup_event
import recommender.main as main_module
from recommender.models import Product

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("recommender.main.load_products")
def test_startup_event_success(mock_load_products):
    mock_load_products.return_value = [1, 2, 3] # Dummy data length
    startup_event()
    assert len(main_module._loaded_products) == 3

@patch("recommender.main.load_products")
def test_startup_event_failure(mock_load_products):
    # Reset first
    main_module._loaded_products = []
    mock_load_products.side_effect = Exception("Test Error")
    startup_event()
    assert len(main_module._loaded_products) == 0

def test_recommend_empty_db():
    main_module._loaded_products = []
    response = client.post("/api/recommend", json={
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
    })
    assert response.status_code == 500
    assert "empty or failed to load" in response.json()["detail"]

@patch("recommender.main.score_products")
def test_recommend_success(mock_score_products):
    mock_score_products.return_value = []
    
    # We need to set a dummy product to bypass the empty check
    main_module._loaded_products = ["dummy"]
    
    response = client.post("/api/recommend", json={
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
    })
    
    assert response.status_code == 200
    assert response.json() == []
