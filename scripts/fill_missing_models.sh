#!/bin/bash
# Fill missing STEP models by:
# 1. Copying near-matches from existing downloads
# 2. Downloading remaining from EasyEDA API using footprint-to-LCSC search

PROJ_DIR="/Users/nils/Downloads/tryingkicadimport"
MODELS_DIR="$PROJ_DIR/EASYEDA_MODELS"
VENV="$PROJ_DIR/.venv/bin/activate"

source "$VENV"

# Get list of missing models
grep -roh '"${KIPRJMOD}/EASYEDA_MODELS/[^"]*"' "$PROJ_DIR/5v rail smart enable.pretty/" "$PROJ_DIR/5v rail smart enable.kicad_pcb" 2>/dev/null \
  | sort -u | sed 's|"${KIPRJMOD}/EASYEDA_MODELS/||;s|"||g' > /tmp/needed_models.txt
ls "$MODELS_DIR/"*.step 2>/dev/null | xargs -n1 basename > /tmp/downloaded_models.txt

MISSING=$(comm -23 /tmp/needed_models.txt /tmp/downloaded_models.txt)
MISSING_COUNT=$(echo "$MISSING" | wc -l | tr -d ' ')

echo "=== Phase 1: Copy near-match models ==="
echo "$MISSING_COUNT models still missing"
echo ""

COPIED=0
STILL_MISSING=""

while IFS= read -r needed; do
    [ -z "$needed" ] && continue
    # Already exists?
    [ -f "$MODELS_DIR/$needed" ] && continue

    base="${needed%.step}"

    # Try exact copy strategies for known patterns:

    # Pattern: FOO-1.step -> try FOO.step
    alt="${base%-1}.step"
    if [ -f "$MODELS_DIR/$alt" ] && [ "$alt" != "$needed" ]; then
        cp "$MODELS_DIR/$alt" "$MODELS_DIR/$needed"
        echo "  COPY: $needed <- $alt"
        COPIED=$((COPIED+1))
        continue
    fi

    # Pattern: USB-C_SMD-TYPE-C-31-M-12.step -> USB-C_SMD-TYPE-C-31-M-12_1.step
    alt="${base}_1.step"
    if [ -f "$MODELS_DIR/$alt" ]; then
        cp "$MODELS_DIR/$alt" "$MODELS_DIR/$needed"
        echo "  COPY: $needed <- $alt"
        COPIED=$((COPIED+1))
        continue
    fi

    # Try fuzzy match: same prefix up to first dimension difference
    prefix=$(echo "$base" | sed 's/_L[0-9].*//;s/_H[0-9].*//;s/_BD[0-9].*//')
    if [ -n "$prefix" ] && [ "$prefix" != "$base" ]; then
        match=$(ls "$MODELS_DIR/" 2>/dev/null | grep "^${prefix}" | head -1)
        if [ -n "$match" ]; then
            cp "$MODELS_DIR/$match" "$MODELS_DIR/$needed"
            echo "  FUZZY: $needed <- $match"
            COPIED=$((COPIED+1))
            continue
        fi
    fi

    STILL_MISSING="$STILL_MISSING
$needed"
done <<< "$MISSING"

echo ""
echo "Phase 1 complete: copied $COPIED near-matches"

# Phase 2: Search EasyEDA for remaining missing models
STILL_MISSING=$(echo "$STILL_MISSING" | sed '/^$/d')
REMAINING=$(echo "$STILL_MISSING" | wc -l | tr -d ' ')
echo ""
echo "=== Phase 2: Search EasyEDA API for $REMAINING remaining models ==="
echo ""

DOWNLOADED=0
FAILED_LIST=""

while IFS= read -r needed; do
    [ -z "$needed" ] && continue
    [ -f "$MODELS_DIR/$needed" ] && continue

    base="${needed%.step}"
    # Extract a search keyword from the model name
    # Remove dimension suffixes to get a cleaner search term
    search_term=$(echo "$base" | sed 's/_L[0-9].*//;s/_H[0-9].*//;s/_BD[0-9].*//;s/_P[0-9].*//')

    echo -n "  [$needed] searching '$search_term'... "

    # Search EasyEDA for a component with this package
    RESPONSE=$(curl -s "https://easyeda.com/api/components?type=2&keyword=${search_term}&version=6.4.19.5" \
        -H "User-Agent: easyeda2kicad" 2>/dev/null)

    # Try to extract first LCSC ID from search results
    LCSC_ID=$(echo "$RESPONSE" | jq -r '.result[0].szlcsc // .result[0].lcsc // empty' 2>/dev/null | head -1)

    if [ -n "$LCSC_ID" ] && [ "$LCSC_ID" != "null" ]; then
        echo -n "found $LCSC_ID, downloading... "
        OUTPUT=$(easyeda2kicad --lcsc_id "$LCSC_ID" --3d --output "$PROJ_DIR/_temp_search" 2>&1)

        if echo "$OUTPUT" | grep -q "Created 3D model"; then
            MODEL_NAME=$(echo "$OUTPUT" | grep "3D model name:" | sed 's/.*3D model name: //')
            STEP_FILE="$PROJ_DIR/_temp_search.3dshapes/${MODEL_NAME}.step"
            if [ -f "$STEP_FILE" ]; then
                cp "$STEP_FILE" "$MODELS_DIR/$needed"
                echo "OK"
                DOWNLOADED=$((DOWNLOADED+1))
            else
                echo "FAIL (file not found)"
                FAILED_LIST="$FAILED_LIST
$needed"
            fi
        else
            echo "FAIL (no 3D model)"
            FAILED_LIST="$FAILED_LIST
$needed"
        fi
        rm -rf "$PROJ_DIR/_temp_search.3dshapes" "$PROJ_DIR/_temp_search.pretty" "$PROJ_DIR/_temp_search.kicad_sym"
    else
        echo "no LCSC match"
        FAILED_LIST="$FAILED_LIST
$needed"
    fi

    sleep 0.5
done <<< "$STILL_MISSING"

echo ""
echo "================================================"
echo "Phase 2 complete: downloaded $DOWNLOADED additional models"

FAILED_LIST=$(echo "$FAILED_LIST" | sed '/^$/d')
FINAL_MISSING=$(echo "$FAILED_LIST" | wc -l | tr -d ' ')

if [ -n "$FAILED_LIST" ]; then
    echo ""
    echo "=== Still missing ($FINAL_MISSING models) ==="
    echo "$FAILED_LIST"
fi

echo ""
echo "Final count in EASYEDA_MODELS: $(ls "$MODELS_DIR/"*.step 2>/dev/null | wc -l | tr -d ' ') models"
