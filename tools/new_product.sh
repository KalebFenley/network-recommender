#!/bin/bash
# tools/new_product.sh
# Scaffold a new product YAML from the template.
#
# Usage: ./tools/new_product.sh <vendor> <model>
# Example: ./tools/new_product.sh arista 7050sx3-48yc12
#
# The script will:
#  1. Generate a slug (e.g. arista-7050sx3-48yc12)
#  2. Copy the template into products/<slug>.yaml
#  3. Pre-fill the id, vendor, and model fields
#  4. Open the file in your $EDITOR (or nano if unset)

set -euo pipefail

VENDOR="${1:-}"
MODEL="${2:-}"

if [[ -z "$VENDOR" || -z "$MODEL" ]]; then
    echo "Usage: $0 <vendor> <model>"
    echo "  Example: $0 arista 7050sx3-48yc12"
    exit 1
fi

# Normalize to lowercase, replace spaces/underscores with hyphens
VENDOR_SLUG=$(echo "$VENDOR" | tr '[:upper:]' '[:lower:]' | tr ' _' '-')
MODEL_SLUG=$(echo "$MODEL"  | tr '[:upper:]' '[:lower:]' | tr ' _' '-')
SLUG="${VENDOR_SLUG}-${MODEL_SLUG}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$REPO_ROOT/products/_template.yaml"
OUT="$REPO_ROOT/products/${SLUG}.yaml"

if [[ ! -f "$TEMPLATE" ]]; then
    echo "ERROR: Template not found at $TEMPLATE"
    exit 1
fi

if [[ -f "$OUT" ]]; then
    echo "ERROR: $OUT already exists. Edit it directly."
    exit 1
fi

# Copy template and pre-fill id, vendor, model
sed \
    -e "s|^id: vendor-model|id: ${SLUG}|" \
    -e "s|^vendor: Vendor Name|vendor: ${VENDOR}|" \
    -e "s|^model: Model Name|model: ${MODEL}|" \
    "$TEMPLATE" > "$OUT"

echo "Created: $OUT"
echo ""
echo "Fields to fill in:"
echo "  - product_line"
echo "  - category  (core-router | edge-router | peering-router | aggregation | access)"
echo "  - interfaces (400G / 100G / 40G / 10G / 1G port counts)"
echo "  - capabilities (backhaul speed, BGP, VRFs, routes, feature flags)"
echo "  - scale (max_bandwidth_Tbps)"
echo "  - os, licensing, notes, links.datasheet"
echo ""

EDITOR="${EDITOR:-nano}"
"$EDITOR" "$OUT"
