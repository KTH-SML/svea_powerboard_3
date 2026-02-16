#!/bin/bash
# Download all 3D STEP models from EasyEDA using LCSC part numbers
# Models are saved to EASYEDA_MODELS/ directory

PROJ_DIR="/Users/nils/Downloads/tryingkicadimport"
MODELS_DIR="$PROJ_DIR/EASYEDA_MODELS"
TEMP_DIR="$PROJ_DIR/_temp_3d_download"
VENV="$PROJ_DIR/.venv/bin/activate"

mkdir -p "$MODELS_DIR"
mkdir -p "$TEMP_DIR"

source "$VENV"

# All unique LCSC part numbers from the schematics
LCSC_PARTS=(
C102646 C102691 C105578 C106224 C106225 C106227 C106259 C106794
C107083 C110251 C113257 C114633 C11702 C122837 C124129 C126612
C127273 C12891 C131334 C1356615 C137723 C138066 C138153 C140087
C144198 C14663 C14665 C151135 C151348 C154726 C15725 C158012
C15849 C165230 C165948 C173406 C173427 C178260 C17901 C181255
C1848315 C1850279 C188252 C19077426 C19077584 C193237 C19330
C19626224 C19829539 C20940299 C21189 C22367835 C22371298
C22371533 C22446827 C22775 C22827 C22860 C22913 C22923 C22933
C22935 C22956 C22962 C23162 C23196 C23231 C23346 C24833806
C25079 C25123 C25741 C25744 C25803 C25804 C25819 C264473
C2678753 C2681220 C270345 C270365 C270366 C270817 C274872
C2765186 C2802562 C281756 C282317 C282519 C2843670 C2846043
C2870135 C2886899 C2898715 C2906859 C2906860 C2906877 C2906974
C2906982 C2906986 C2907002 C2907012 C2907025 C2907044 C2907072
C2907088 C2907089 C2907091 C2907172 C2907174 C2930080 C2930095
C2930175 C2933128 C2933239 C2941042 C295786 C295802 C2960716
C2977552 C2999532 C3000497 C3013343 C3032176 C307331 C3151829
C319050 C321081 C3289459 C32998 C33002 C3335788 C344195 C347476
C353315 C3646921 C3682863 C4184 C4190 C42441843 C431533 C440198
C45783 C461078 C468683 C473393 C473458 C475504 C481766 C49164689
C492401 C49256794 C49851 C5126099 C5137573 C5142551 C5199872
C5205497 C5221836 C5224154 C5246541 C5260346 C53114384 C5379879
C5440143 C5775686 C603785 C6119852 C6119901 C64705 C668119
C66886 C674416 C690729 C696861 C698148 C7073593 C7125816 C720075
C720477 C72473 C7250 C72505 C72519 C72523 C727061 C7420012
C7420332 C7429379 C7429632 C7429643 C7429669 C7430409 C7436903
C74710 C76854 C76925 C77572 C77905 C80160 C83152 C84263 C86295
C875732 C908770 C92759 C92814 C98192 C98732 C9900015874
)

TOTAL=${#LCSC_PARTS[@]}
SUCCESS=0
FAILED=0
SKIPPED=0

echo "Starting download of 3D models for $TOTAL LCSC parts..."
echo "Models will be saved to: $MODELS_DIR"
echo "================================================"

for i in "${!LCSC_PARTS[@]}"; do
    PART="${LCSC_PARTS[$i]}"
    NUM=$((i + 1))

    echo -n "[$NUM/$TOTAL] $PART ... "

    # Download to temp directory
    OUTPUT=$(easyeda2kicad --lcsc_id "$PART" --3d --output "$TEMP_DIR/temp_dl" 2>&1)

    if echo "$OUTPUT" | grep -q "Created 3D model"; then
        # Extract the model name from output
        MODEL_NAME=$(echo "$OUTPUT" | grep "3D model name:" | sed 's/.*3D model name: //')

        # Move STEP file to EASYEDA_MODELS
        STEP_FILE="$TEMP_DIR/temp_dl.3dshapes/${MODEL_NAME}.step"
        if [ -f "$STEP_FILE" ]; then
            if [ -f "$MODELS_DIR/${MODEL_NAME}.step" ]; then
                echo "SKIP (already exists: ${MODEL_NAME}.step)"
                SKIPPED=$((SKIPPED + 1))
            else
                cp "$STEP_FILE" "$MODELS_DIR/${MODEL_NAME}.step"
                echo "OK -> ${MODEL_NAME}.step"
                SUCCESS=$((SUCCESS + 1))
            fi
        else
            echo "FAIL (file not found after download)"
            FAILED=$((FAILED + 1))
        fi
    else
        # Check for specific errors
        if echo "$OUTPUT" | grep -q "No 3D model"; then
            echo "SKIP (no 3D model available)"
            SKIPPED=$((SKIPPED + 1))
        else
            echo "FAIL"
            echo "  Error: $(echo "$OUTPUT" | tail -1)"
            FAILED=$((FAILED + 1))
        fi
    fi

    # Clean temp files
    rm -rf "$TEMP_DIR/temp_dl.3dshapes" "$TEMP_DIR/temp_dl.pretty" "$TEMP_DIR/temp_dl.kicad_sym"

    # Small delay to avoid rate limiting
    sleep 0.3
done

echo ""
echo "================================================"
echo "Download complete!"
echo "  Success: $SUCCESS"
echo "  Skipped: $SKIPPED"
echo "  Failed:  $FAILED"
echo ""
echo "Models saved to: $MODELS_DIR"
echo "Total files: $(ls "$MODELS_DIR"/*.step 2>/dev/null | wc -l)"

# Clean up temp
rm -rf "$TEMP_DIR"
