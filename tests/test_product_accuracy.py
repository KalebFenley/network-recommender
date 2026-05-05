"""
Semantic accuracy tests for product YAML files.

These tests go beyond YAML syntax and Pydantic schema checks to validate
logical consistency and real-world plausibility of the hardware data.
They act as a sanity net to catch copy-paste errors, incorrect values,
or missing fields when new products are added.
"""
import pytest
import yaml
from pathlib import Path
from recommender.models import Product

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

PRODUCTS_DIR = Path(__file__).parent.parent / "products"

BOOL_CAPABILITY_FIELDS = [
    "full_bgp_table", "mpls", "segment_routing", "evpn",
    "bng", "ptp", "macsec", "nat", "openconfig", "streaming_telemetry",
]

VALID_CATEGORIES = {"core-router", "edge-router", "peering-router", "aggregation", "access"}
VALID_LICENSING = {"perpetual", "subscription", "mixed"}

# Full-BGP-table platforms should have at least this many IPv4 routes.
FULL_BGP_MIN_ROUTES = 1_000_000
# Sanity floor: no product should claim sub-1G backhaul
MIN_BACKHAUL_G = 1
# Sanity ceiling: nothing credible exceeds 1000 Tbps today
MAX_BANDWIDTH_TBPS = 1000.0


def load_products() -> list[tuple[str, Product]]:
    """Load all non-template product YAML files as (filename, Product) tuples."""
    results = []
    for path in sorted(PRODUCTS_DIR.glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        product = Product.model_validate(data)
        results.append((path.name, product))
    return results


ALL_PRODUCTS = load_products()
PRODUCT_IDS = [fname for fname, _ in ALL_PRODUCTS]


def pytest_generate_tests(metafunc):
    """Parametrize any test that accepts the 'product_fixture' fixture."""
    if "product_fixture" in metafunc.fixturenames:
        metafunc.parametrize(
            "product_fixture",
            ALL_PRODUCTS,
            ids=PRODUCT_IDS,
        )


# ---------------------------------------------------------------------------
# Schema presence tests
# ---------------------------------------------------------------------------

class TestRequiredFields:
    """Every product must have a complete, non-empty set of top-level fields."""

    def test_id_is_non_empty(self, product_fixture):
        """Product id must be a non-empty string."""
        _, product = product_fixture
        assert product.id and isinstance(product.id, str), \
            f"Product id is empty or missing"

    def test_vendor_is_non_empty(self, product_fixture):
        """Vendor field must be a non-empty string."""
        _, product = product_fixture
        assert product.vendor and isinstance(product.vendor, str)

    def test_model_is_non_empty(self, product_fixture):
        """Model field must be a non-empty string."""
        _, product = product_fixture
        assert product.model and isinstance(product.model, str)

    def test_category_is_valid(self, product_fixture):
        """Category must be one of the defined enum values."""
        _, product = product_fixture
        assert product.category in VALID_CATEGORIES, \
            f"Unknown category '{product.category}'"

    def test_notes_is_non_empty(self, product_fixture):
        """Notes field must contain a meaningful description."""
        _, product = product_fixture
        assert product.notes and len(product.notes.strip()) > 20, \
            "Notes field is missing or too short"

    def test_licensing_model_is_valid(self, product_fixture):
        """Licensing model must be perpetual, subscription, or mixed."""
        _, product = product_fixture
        assert product.licensing.model in VALID_LICENSING

    def test_nat_field_present(self, product_fixture):
        """Every product must explicitly declare nat capability."""
        _, product = product_fixture
        assert hasattr(product.capabilities, "nat"), \
            "nat field is missing from capabilities"
        assert isinstance(product.capabilities.nat, bool), \
            "nat must be a boolean"

    def test_all_bool_capabilities_are_present(self, product_fixture):
        """All expected boolean capability keys must exist on every product."""
        _, product = product_fixture
        caps = product.capabilities
        for field in BOOL_CAPABILITY_FIELDS:
            assert hasattr(caps, field), \
                f"Missing capability field: {field}"
            assert isinstance(getattr(caps, field), bool), \
                f"Capability '{field}' must be a boolean"


# ---------------------------------------------------------------------------
# Numeric range sanity tests
# ---------------------------------------------------------------------------

class TestNumericRanges:
    """Values must fall within physically plausible ranges."""

    def test_max_backhaul_G_is_positive(self, product_fixture):
        """max_backhaul_G must be a positive integer."""
        _, product = product_fixture
        assert product.capabilities.max_backhaul_G >= MIN_BACKHAUL_G, \
            f"max_backhaul_G={product.capabilities.max_backhaul_G} is too low"

    def test_max_bgp_peers_is_positive(self, product_fixture):
        """max_bgp_peers must be a positive integer."""
        _, product = product_fixture
        assert product.capabilities.max_bgp_peers > 0

    def test_max_vrfs_is_positive(self, product_fixture):
        """max_vrfs must be a positive integer."""
        _, product = product_fixture
        assert product.capabilities.max_vrfs > 0

    def test_max_ipv4_routes_is_positive(self, product_fixture):
        """max_ipv4_routes must be a positive integer."""
        _, product = product_fixture
        assert product.capabilities.max_ipv4_routes > 0

    def test_max_bandwidth_is_positive(self, product_fixture):
        """max_bandwidth_Tbps must be a positive, credible value."""
        _, product = product_fixture
        bw = product.scale.max_bandwidth_Tbps
        assert 0 < bw <= MAX_BANDWIDTH_TBPS, \
            f"max_bandwidth_Tbps={bw} is outside plausible range (0, {MAX_BANDWIDTH_TBPS}]"

    def test_all_interface_counts_non_negative(self, product_fixture):
        """No interface count may be negative."""
        _, product = product_fixture
        ifaces = product.interfaces
        for speed, count in [
            ("400G", ifaces.speed_400G),
            ("100G", ifaces.speed_100G),
            ("40G", ifaces.speed_40G),
            ("10G", ifaces.speed_10G),
            ("1G", ifaces.speed_1G),
        ]:
            assert count >= 0, f"{speed} interface count is negative ({count})"

    def test_at_least_one_interface_type_populated(self, product_fixture):
        """Every product must have at least one interface port defined."""
        _, product = product_fixture
        ifaces = product.interfaces
        total = (
            ifaces.speed_400G + ifaces.speed_100G + ifaces.speed_40G
            + ifaces.speed_10G + ifaces.speed_1G
        )
        assert total > 0, "Product has zero interfaces across all speeds"

    def test_subscriber_scale_is_positive_when_set(self, product_fixture):
        """subscriber_scale, if set, must be a positive integer."""
        _, product = product_fixture
        ss = product.scale.subscriber_scale
        if ss is not None:
            assert ss > 0, f"subscriber_scale={ss} must be positive"


# ---------------------------------------------------------------------------
# Cross-field consistency tests
# ---------------------------------------------------------------------------

class TestCrossFieldConsistency:
    """Logical consistency rules that span multiple fields."""

    def test_full_bgp_table_implies_sufficient_routes(self, product_fixture):
        """If full_bgp_table is True, ipv4 routes must cover the internet table."""
        _, product = product_fixture
        if product.capabilities.full_bgp_table:
            routes = product.capabilities.max_ipv4_routes
            assert routes >= FULL_BGP_MIN_ROUTES, (
                f"full_bgp_table=True but max_ipv4_routes={routes:,} "
                f"is below the {FULL_BGP_MIN_ROUTES:,} minimum for a full BGP table"
            )

    def test_bng_implies_subscriber_scale(self, product_fixture):
        """BNG-capable platforms should have a subscriber_scale value set."""
        _, product = product_fixture
        if product.capabilities.bng:
            assert product.scale.subscriber_scale is not None, (
                "bng=True but subscriber_scale is null — set an expected subscriber limit"
            )

    def test_core_router_has_full_bgp_table(self, product_fixture):
        """Core routers are expected to support the full internet BGP table."""
        fname, product = product_fixture
        if product.category == "core-router":
            assert product.capabilities.full_bgp_table is True, (
                f"{fname}: category=core-router but full_bgp_table=False"
            )

    def test_access_router_not_claiming_full_bgp_table(self, product_fixture):
        """Access-tier devices should not claim to carry the full BGP table."""
        fname, product = product_fixture
        if product.category == "access":
            assert product.capabilities.full_bgp_table is False, (
                f"{fname}: category=access but full_bgp_table=True — "
                "access devices don't carry the internet routing table"
            )

    def test_nat_true_only_on_service_capable_categories(self, product_fixture):
        """
        NAT is a service-layer feature — pure core platforms shouldn't advertise it.

        We flag this as a warning-level check: core-routers with nat=True likely
        have an incorrect value since hardware NAT at core scale is almost never
        supported.
        """
        fname, product = product_fixture
        if product.capabilities.nat and product.category == "core-router":
            pytest.fail(
                f"{fname}: nat=True on a core-router is unexpected. "
                "Core routers don't perform NAT. If intentional, add a note."
            )

    def test_segment_routing_implies_mpls_or_srv6(self, product_fixture):
        """
        Segment Routing depends on an underlying transport.
        If SR is enabled, MPLS should also be enabled (SRv6-only platforms are
        a valid exception, but none in this catalog are SRv6-only).
        """
        fname, product = product_fixture
        if product.capabilities.segment_routing:
            assert product.capabilities.mpls is True, (
                f"{fname}: segment_routing=True but mpls=False — "
                "verify whether this platform uses SR-MPLS or SRv6 and update accordingly"
            )

    def test_bandwidth_consistent_with_port_count(self, product_fixture):
        """
        Aggregate interface bandwidth should not wildly exceed claimed system capacity.
        This catches typos like 32x400G ports but max_bandwidth_Tbps=1.0.

        Note: Modular chassis products (core-routers with slot-based models) list ports
        for a representative line card config, not the full chassis, so the system
        max_bandwidth_Tbps will legitimately exceed the per-card port count. These
        are skipped here and validated by reading the datasheet instead.
        """
        fname, product = product_fixture
        # Modular chassis: interfaces represent one line card, not the full system.
        # Their bandwidth spec covers all slots filled, which will always exceed
        # a single line card's theoretical port bandwidth.
        if product.category == "core-router" and (
            "slot" in product.model.lower() or "chassis" in product.model.lower()
        ):
            pytest.skip(
                f"Skipping bandwidth check for modular chassis '{fname}' — "
                "interfaces represent one line card; system BW covers full chassis."
            )

        ifaces = product.interfaces
        # Compute a naive upper bound: assume every port runs at its labeled speed
        theoretical_tbps = (
            ifaces.speed_400G * 0.4
            + ifaces.speed_100G * 0.1
            + ifaces.speed_40G * 0.04
            + ifaces.speed_10G * 0.01
            + ifaces.speed_1G * 0.001
        )
        bw = product.scale.max_bandwidth_Tbps
        # Allow 2x margin for fabric oversubscription models
        assert bw <= theoretical_tbps * 2 or theoretical_tbps == 0, (
            f"max_bandwidth_Tbps={bw} Tbps seems too high for the listed interfaces "
            f"(theoretical max ~{theoretical_tbps:.1f} Tbps). Check port counts or bandwidth."
        )
        # Also check the floor: bandwidth shouldn't be less than the fastest single port
        max_single_port_tbps = max(
            (0.4 if ifaces.speed_400G else 0),
            (0.1 if ifaces.speed_100G else 0),
            (0.04 if ifaces.speed_40G else 0),
            (0.01 if ifaces.speed_10G else 0),
            (0.001 if ifaces.speed_1G else 0),
        )
        assert bw >= max_single_port_tbps, (
            f"max_bandwidth_Tbps={bw} Tbps is less than a single port's speed "
            f"({max_single_port_tbps} Tbps) — check the value"
        )


# ---------------------------------------------------------------------------
# ID / filename consistency tests
# ---------------------------------------------------------------------------

class TestNamingConventions:
    """Filename and ID should be consistent so the catalog is navigable."""

    def test_id_matches_filename(self, product_fixture):
        """Product id should match the YAML filename (without .yaml extension)."""
        fname, product = product_fixture
        expected_id = fname.replace(".yaml", "")
        assert product.id == expected_id, (
            f"Filename '{fname}' does not match id='{product.id}'. "
            "They should be identical for consistent catalog lookups."
        )

    def test_id_is_lowercase_hyphenated(self, product_fixture):
        """Product id must be lowercase and hyphen-separated (no spaces or underscores)."""
        _, product = product_fixture
        assert product.id == product.id.lower(), "id must be lowercase"
        assert " " not in product.id, "id must not contain spaces"
        assert "_" not in product.id, "id must not contain underscores; use hyphens"
