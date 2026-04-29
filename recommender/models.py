"""
Pydantic models for the Network Hardware Recommendation Engine.
"""
from typing import Optional, Literal, Dict
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class Interfaces(BaseModel):
    """Interface counts by speed."""
    model_config = ConfigDict(populate_by_name=True)
    
    speed_400G: int = Field(alias="400G", default=0)
    speed_100G: int = Field(alias="100G", default=0)
    speed_40G: int = Field(alias="40G", default=0)
    speed_10G: int = Field(alias="10G", default=0)
    speed_1G: int = Field(alias="1G", default=0)

class Capabilities(BaseModel):
    """Routing, feature, and scale capabilities of the product."""
    max_backhaul_G: int
    full_bgp_table: bool
    max_bgp_peers: int
    max_vrfs: int
    max_ipv4_routes: int
    mpls: bool
    segment_routing: bool
    evpn: bool
    bng: bool
    ptp: bool
    macsec: bool
    openconfig: bool
    streaming_telemetry: bool

class Scale(BaseModel):
    """Bandwidth and subscriber scale."""
    max_bandwidth_Tbps: float
    subscriber_scale: Optional[int] = None

class Licensing(BaseModel):
    """Software licensing details."""
    model: Literal["perpetual", "subscription", "mixed"]
    notes: str

class Links(BaseModel):
    """Relevant product links."""
    datasheet: Optional[HttpUrl] = None
    product_page: Optional[HttpUrl] = None

class Product(BaseModel):
    """Network hardware product definition."""
    id: str
    vendor: str
    product_line: str
    model: str
    category: Literal["core-router", "edge-router", "peering-router", "aggregation", "access"]
    interfaces: Interfaces
    capabilities: Capabilities
    scale: Scale
    os: str
    licensing: Licensing
    notes: str
    links: Links

class Questionnaire(BaseModel):
    """User answers from the recommendation questionnaire."""
    # Capacity
    required_backhaul_G: int
    min_400G: int = 0
    min_100G: int = 0
    min_40G: int = 0
    min_10G: int = 0
    min_1G: int = 0

    # Routing scale
    full_bgp_table: bool
    min_bgp_peers: int
    min_vrfs: int
    min_ipv4_routes: int

    # Traffic profile
    peak_bandwidth_Tbps: float
    role: Literal["core-router", "edge-router", "peering-router", "aggregation", "access"]
    needs_mpls: bool
    needs_segment_routing: bool

    # Subscriber scale
    needs_bng: bool
    subscribers_5yr: Optional[int] = None
    
    # Features
    needs_evpn: bool
    needs_ptp: bool
    needs_macsec: bool
    needs_openconfig: bool
    needs_streaming_telemetry: bool

    # Operational
    preferred_os: Optional[str] = None
    
    # Licensing preference
    preferred_licensing: Literal["perpetual", "subscription", "mixed", "no-preference"] = "no-preference"
