import yaml
from pathlib import Path

products = [
    {
        "id": "cisco-8201-32fh", "vendor": "Cisco", "product_line": "8000 Series", "model": "8201-32FH", "category": "core-router",
        "interfaces": {"400G": 32, "100G": 0, "40G": 0, "10G": 0, "1G": 0},
        "capabilities": {"max_backhaul_G": 400, "full_bgp_table": True, "max_bgp_peers": 4000, "max_vrfs": 4000, "max_ipv4_routes": 4000000, "mpls": True, "segment_routing": True, "evpn": True, "bng": False, "ptp": True, "macsec": True, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 12.8, "subscriber_scale": None},
        "os": "IOS-XR", "licensing": {"model": "subscription", "notes": "Requires Smart Licensing."}, "notes": "Strong fit for core and peering roles.", "links": {}
    },
    {
        "id": "juniper-ptx10001-36mr", "vendor": "Juniper", "product_line": "PTX Series", "model": "PTX10001-36MR", "category": "core-router",
        "interfaces": {"400G": 24, "100G": 12, "40G": 0, "10G": 0, "1G": 0},
        "capabilities": {"max_backhaul_G": 400, "full_bgp_table": True, "max_bgp_peers": 4000, "max_vrfs": 4000, "max_ipv4_routes": 4000000, "mpls": True, "segment_routing": True, "evpn": True, "bng": False, "ptp": True, "macsec": True, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 9.6, "subscriber_scale": None},
        "os": "JunOS", "licensing": {"model": "mixed", "notes": "Base OS perpetual, advanced features subscription."}, "notes": "High-density core router.", "links": {}
    },
    {
        "id": "juniper-mx204", "vendor": "Juniper", "product_line": "MX Series", "model": "MX204", "category": "edge-router",
        "interfaces": {"400G": 0, "100G": 4, "40G": 0, "10G": 8, "1G": 0},
        "capabilities": {"max_backhaul_G": 100, "full_bgp_table": True, "max_bgp_peers": 2000, "max_vrfs": 2000, "max_ipv4_routes": 2000000, "mpls": True, "segment_routing": True, "evpn": True, "bng": True, "ptp": True, "macsec": True, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 0.4, "subscriber_scale": 32000},
        "os": "JunOS", "licensing": {"model": "mixed", "notes": "Flex licensing for advanced features."}, "notes": "Versatile edge and peering router.", "links": {}
    },
    {
        "id": "nokia-7750-sr-1x-48d", "vendor": "Nokia", "product_line": "7750 SR", "model": "7750 SR-1x-48D", "category": "edge-router",
        "interfaces": {"400G": 48, "100G": 0, "40G": 0, "10G": 0, "1G": 0},
        "capabilities": {"max_backhaul_G": 400, "full_bgp_table": True, "max_bgp_peers": 5000, "max_vrfs": 5000, "max_ipv4_routes": 5000000, "mpls": True, "segment_routing": True, "evpn": True, "bng": True, "ptp": True, "macsec": True, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 19.2, "subscriber_scale": 128000},
        "os": "SR OS", "licensing": {"model": "subscription", "notes": "Feature packs required."}, "notes": "High scale BNG and Edge.", "links": {}
    },
    {
        "id": "arista-7280cr3-32p4", "vendor": "Arista", "product_line": "7280R3 Series", "model": "7280CR3-32P4", "category": "peering-router",
        "interfaces": {"400G": 4, "100G": 32, "40G": 0, "10G": 0, "1G": 0},
        "capabilities": {"max_backhaul_G": 400, "full_bgp_table": True, "max_bgp_peers": 3000, "max_vrfs": 2000, "max_ipv4_routes": 2000000, "mpls": True, "segment_routing": True, "evpn": True, "bng": False, "ptp": True, "macsec": True, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 4.8, "subscriber_scale": None},
        "os": "EOS", "licensing": {"model": "perpetual", "notes": "Perpetual OS license."}, "notes": "Deep buffer peering switch.", "links": {}
    },
    {
        "id": "cisco-asr9901", "vendor": "Cisco", "product_line": "ASR 9000 Series", "model": "ASR 9901", "category": "edge-router",
        "interfaces": {"400G": 0, "100G": 2, "40G": 0, "10G": 24, "1G": 0},
        "capabilities": {"max_backhaul_G": 100, "full_bgp_table": True, "max_bgp_peers": 2000, "max_vrfs": 2000, "max_ipv4_routes": 2000000, "mpls": True, "segment_routing": True, "evpn": True, "bng": True, "ptp": True, "macsec": True, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 0.456, "subscriber_scale": 64000},
        "os": "IOS-XR", "licensing": {"model": "subscription", "notes": "Smart Licensing required."}, "notes": "Compact edge router with full BNG.", "links": {}
    },
    {
        "id": "huawei-ne8000-m8", "vendor": "Huawei", "product_line": "NetEngine 8000", "model": "NE8000 M8", "category": "aggregation",
        "interfaces": {"400G": 0, "100G": 8, "40G": 0, "10G": 48, "1G": 0},
        "capabilities": {"max_backhaul_G": 100, "full_bgp_table": True, "max_bgp_peers": 1000, "max_vrfs": 1000, "max_ipv4_routes": 1000000, "mpls": True, "segment_routing": True, "evpn": True, "bng": True, "ptp": True, "macsec": False, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 1.2, "subscriber_scale": 32000},
        "os": "VRP", "licensing": {"model": "mixed", "notes": "Base + features."}, "notes": "Aggregation and edge.", "links": {}
    },
    {
        "id": "arista-7050cx3", "vendor": "Arista", "product_line": "7050X3 Series", "model": "7050CX3-32S", "category": "aggregation",
        "interfaces": {"400G": 0, "100G": 32, "40G": 0, "10G": 0, "1G": 0},
        "capabilities": {"max_backhaul_G": 100, "full_bgp_table": False, "max_bgp_peers": 100, "max_vrfs": 64, "max_ipv4_routes": 128000, "mpls": False, "segment_routing": False, "evpn": True, "bng": False, "ptp": True, "macsec": False, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 3.2, "subscriber_scale": None},
        "os": "EOS", "licensing": {"model": "perpetual", "notes": "Perpetual."}, "notes": "Leaf switch.", "links": {}
    },
    {
        "id": "cisco-ncs5501", "vendor": "Cisco", "product_line": "NCS 5500 Series", "model": "NCS 5501", "category": "peering-router",
        "interfaces": {"400G": 0, "100G": 4, "40G": 0, "10G": 48, "1G": 0},
        "capabilities": {"max_backhaul_G": 100, "full_bgp_table": True, "max_bgp_peers": 2000, "max_vrfs": 2000, "max_ipv4_routes": 1500000, "mpls": True, "segment_routing": True, "evpn": True, "bng": False, "ptp": True, "macsec": True, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 0.8, "subscriber_scale": None},
        "os": "IOS-XR", "licensing": {"model": "subscription", "notes": "Smart License."}, "notes": "Cost-effective peering.", "links": {}
    },
    {
        "id": "nokia-7250-ixr-e", "vendor": "Nokia", "product_line": "7250 IXR", "model": "7250 IXR-e", "category": "access",
        "interfaces": {"400G": 0, "100G": 2, "40G": 0, "10G": 14, "1G": 8},
        "capabilities": {"max_backhaul_G": 100, "full_bgp_table": False, "max_bgp_peers": 100, "max_vrfs": 256, "max_ipv4_routes": 256000, "mpls": True, "segment_routing": True, "evpn": True, "bng": False, "ptp": True, "macsec": True, "openconfig": True, "streaming_telemetry": True},
        "scale": {"max_bandwidth_Tbps": 0.3, "subscriber_scale": None},
        "os": "SR OS", "licensing": {"model": "subscription", "notes": "Feature packs."}, "notes": "Access/Cell site router.", "links": {}
    }
]

out_dir = Path("products")
out_dir.mkdir(exist_ok=True)

for p in products:
    with open(out_dir / f"{p['id']}.yaml", "w") as f:
        yaml.dump(p, f, sort_keys=False)
        
print(f"Seeded {len(products)} products.")
