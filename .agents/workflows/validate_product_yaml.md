# Workflow: Validate Product YAML Accuracy Against Vendor Datasheets

## Purpose

Validate one or more `products/*.yaml` files for **hardware accuracy** —
confirming that every numeric and boolean field matches the official vendor
datasheet, not just that the YAML is syntactically valid.

Run this workflow whenever a new product YAML is created or edited, or on
the full `products/` directory during a periodic audit.

---

## Trigger

Invoke this workflow by saying:

> "Validate the product YAML for `<filename-or-directory>`"
> "Accuracy check `products/arista-7050sx-64.yaml`"
> "Audit all product YAMLs against datasheets"

---

## Inputs

| Input | Description | Example |
|-------|-------------|---------|
| `target` | A single YAML file path or `products/` for all | `products/arista-7050sx-64.yaml` |

If `target` is a directory, process every `*.yaml` file excluding `_template.yaml`.

---

## Steps

### Step 1 — Read the YAML file(s)

Read each target YAML file and extract the following fields for validation:

```
id, vendor, model, product_line, category
interfaces: 400G, 100G, 40G, 10G, 1G
capabilities: max_backhaul_G, full_bgp_table, max_bgp_peers, max_vrfs,
              max_ipv4_routes, mpls, segment_routing, evpn, bng, ptp,
              macsec, nat, openconfig, streaming_telemetry
scale: max_bandwidth_Tbps
links: datasheet
```

---

### Step 2 — Locate the official datasheet

**Priority order for source:**

1. **Fetch `links.datasheet` URL directly** — if the URL resolves and returns
   content, use it as the primary source.
2. **Fetch `links.product_page`** — if datasheet URL fails, try the product page.
3. **Web search fallback** — search for:
   `"<vendor> <model> datasheet specs site:<vendor-domain>"`.
   Prefer official vendor domains (arista.com, juniper.net, cisco.com,
   nokia.com, huawei.com). Avoid resellers (CDW, Newegg, etc.) as a primary
   source, but use them to cross-reference if the vendor site blocks access.

> **Important:** Always note which source was actually used in the report.
> If only a reseller or third-party site was available, flag it as
> lower-confidence.

---

### Step 3 — Validate each field

Check every field below against the datasheet. For each field, record:
- **Status**: `✓ PASS`, `✗ FAIL`, or `~ WARN` (close but uncertain)
- **YAML value**: what the file currently says
- **Datasheet value**: what the official spec actually says
- **Notes**: any important context (e.g., "bidirectional vs one-way")

#### Interface Counts
- Verify native port counts for each speed tier (400G / 100G / 40G / 10G / 1G).
- **Breakout does NOT count.** If a port can be broken out to a lower speed
  but is not natively that speed, it must be counted at its native speed only.
- Flag any port type listed as `> 0` that actually requires a breakout cable.

#### Bandwidth
- `max_bandwidth_Tbps` must be the **one-way / egress** switching capacity.
- Datasheets often quote bidirectional (full-duplex) figures — divide by 2
  if the datasheet says "bidirectional" or "full-duplex".
- Allow ±5% tolerance for rounding.

#### `max_backhaul_G`
- Must equal the highest native single-port speed on the device (not uplink
  aggregate). E.g., a switch with 40G QSFP+ uplinks → `max_backhaul_G: 40`.

#### Routing Scale
- `max_ipv4_routes` — **hardware FIB/TCAM limit**, not the software RIB.
  These are often very different. The FIB limit is what matters for wire-speed
  forwarding. Verify explicitly from the scalability table, not the features list.
- `max_bgp_peers` — verify against the vendor's verified scalability guide if
  available; fall back to the datasheet table.
- `max_vrfs` — same as above.
- `full_bgp_table` — mark `true` only if the hardware FIB can hold a full
  internet routing table (currently ~900k–1M+ IPv4 prefixes). Anything under
  500k FIB routes should be `false`.

#### Boolean Capabilities
For each capability flag, verify against the official feature matrix:

| Field | What to verify |
|-------|----------------|
| `mpls` | Hardware MPLS label switching (not just LDP config) |
| `segment_routing` | SR-MPLS or SRv6 forwarding in hardware |
| `evpn` | EVPN control plane with hardware VTEP |
| `bng` | Broadband Network Gateway / subscriber management |
| `ptp` | IEEE 1588v2 hardware timestamping (not software-only) |
| `macsec` | **Hardware** MACsec (IEEE 802.1AE) — software-only does NOT count |
| `nat` | Hardware NAT (line-rate) |
| `openconfig` | OpenConfig YANG model support via NETCONF/gNMI |
| `streaming_telemetry` | gRPC/gNMI streaming telemetry from hardware counters |

> **MACsec is especially prone to errors.** Many switches support it on
> some generations of ASIC but not others. Always verify the *specific model*,
> not the product line generally.

---

### Step 4 — Produce the validation report

Output a structured report for each file validated:

```
## <filename>

**Source used:** <URL or search query>
**Source type:** Official datasheet / Product page / Reseller (lower confidence)

### Summary
- X fields validated
- X PASS, X FAIL, X WARN

### Field Results

| Field | YAML Value | Datasheet Value | Status | Notes |
|-------|-----------|-----------------|--------|-------|
| interfaces.10G | 48 | 48 | ✓ PASS | |
| macsec | true | false | ✗ FAIL | 7050X2 ASIC lacks hw MACsec |
| max_ipv4_routes | 128000 | 14000 | ✗ FAIL | FIB limit, not RIB |
| max_bandwidth_Tbps | 1.44 | 0.72 | ✗ FAIL | Datasheet quotes full-duplex |

### Corrections Required
List only FAIL items with the exact YAML edit needed:
- `macsec: false`
- `max_ipv4_routes: 14000`
- `max_bandwidth_Tbps: 0.72`
```

---

### Step 5 — Apply corrections

After producing the report:

1. **Apply all `✗ FAIL` corrections** directly to the YAML file(s).
2. **Do not change `~ WARN` fields** without user confirmation — flag them
   explicitly and ask.
3. Re-run `pytest tests/test_product_accuracy.py` to confirm the automated
   consistency checks still pass after edits.

---

### Step 6 — Git actions

After all corrections are applied and tests pass:

1. Create a branch: `fix-product-accuracy-<vendor>-<model>` (or
   `fix-product-accuracy-audit-<date>` for bulk audits).
2. Stage only the corrected YAML file(s).
3. Commit with message:
   ```
   fix(products): accuracy corrections for <model> against official datasheet

   Fields corrected:
   - <field>: <old> → <new> (<reason>)
   ```
4. Push branch, merge to master, delete branch.

---

## Rules and Constraints

- **Never accept a reseller site as the sole source for boolean capability
  flags** (MACsec, MPLS, etc.). Always cross-reference with at least one
  official vendor source.
- **Never add breakout port counts to native port counts.** A 40G port that
  can break out to 4×10G is counted as one 40G port.
- **Never use the bidirectional bandwidth figure** for `max_bandwidth_Tbps`.
  Always halve it if the datasheet quotes a full-duplex number.
- **When in doubt, mark `~ WARN` and ask** rather than silently picking a value.
- If the datasheet URL in the YAML is a 404 or redirects to a generic page,
  update `links.datasheet` to a working URL as part of the fix.

---

## Example Invocations

```
Validate products/arista-7050sx2-128.yaml
Accuracy check all YAMLs in products/
Audit juniper-ex4550-32f.yaml against the vendor datasheet
```
