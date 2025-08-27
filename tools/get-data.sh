#!/bin/bash

# Stripe Synthetic Dataset - Data Fetcher CLI
# Usage: ./tools/get-data.sh <persona> [output_dir]

set -e

# Configuration
REPO_URL="https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/pre_generated_data"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Help function
show_help() {
    echo -e "${BLUE}Stripe Synthetic Dataset - Data Fetcher${NC}"
    echo ""
    echo "Usage: ./tools/get-data.sh <persona> [output_dir]"
    echo ""
    echo "Available personas:"
    echo "  techstyle  - E-commerce fashion retailer"
    echo "  edutech    - Online education marketplace"
    echo ""
    echo "Examples:"
    echo "  ./tools/get-data.sh techstyle"
    echo "  ./tools/get-data.sh edutech ./my-project/data/"
    echo "  ./tools/get-data.sh techstyle --list-files"
    echo ""
    echo "Options:"
    echo "  --list-files  Show available files for persona"
    echo "  --help        Show this help message"
}

# List available personas
list_personas() {
    echo -e "${BLUE}Available Personas:${NC}"
    echo ""
    
    if [ -f "$ROOT_DIR/pre_generated_data/index.json" ]; then
        if command -v jq >/dev/null 2>&1; then
            jq -r '.datasets | to_entries[] | "  \(.key) - \(.value.name)"' "$ROOT_DIR/pre_generated_data/index.json"
        else
            echo "  techstyle - TechStyle Fashion Retailer"
            echo "  edutech   - EduTech Academy"
        fi
    else
        echo "  techstyle - TechStyle Fashion Retailer"
        echo "  edutech   - EduTech Academy"
    fi
    echo ""
}

# List files for a persona
list_files() {
    local persona=$1
    local manifest_url="$REPO_URL/$persona/manifest.json"
    
    echo -e "${BLUE}Available files for $persona:${NC}"
    echo ""
    
    if command -v curl >/dev/null 2>&1; then
        if curl -s "$manifest_url" | head -1 | grep -q "{"; then
            if command -v jq >/dev/null 2>&1; then
                curl -s "$manifest_url" | jq -r '.files | to_entries[] | "  \(.key) - \(.value.description)"'
            else
                echo "  payments.json - Payment transactions"
                echo "  customers.json - Customer profiles"
                echo "  (Install jq for detailed file listing)"
            fi
        else
            echo -e "${RED}  Persona '$persona' not found${NC}"
            return 1
        fi
    else
        echo -e "${RED}  curl not found - please install curl${NC}"
        return 1
    fi
    echo ""
}

# Download files for a persona
download_persona() {
    local persona=$1
    local output_dir=${2:-"./data/$persona"}
    
    # Create output directory
    mkdir -p "$output_dir"
    
    echo -e "${BLUE}Downloading $persona dataset to $output_dir...${NC}"
    echo ""
    
    # Download manifest first
    local manifest_url="$REPO_URL/$persona/manifest.json"
    
    if ! curl -s "$manifest_url" -o "$output_dir/manifest.json"; then
        echo -e "${RED}Failed to download manifest for '$persona'${NC}"
        echo -e "${RED}Available personas: techstyle, edutech${NC}"
        return 1
    fi
    
    # Get file list from manifest
    local files=()
    if command -v jq >/dev/null 2>&1; then
        while IFS= read -r line; do
            files+=("$line")
        done < <(jq -r '.files | keys[]' "$output_dir/manifest.json")
    else
        # Fallback file list
        case $persona in
            techstyle)
                files=("payments.json" "customers.json" "daily_metrics.json" "summary_stats.json")
                ;;
            edutech)
                files=("instructors.json" "students.json" "courses.json" "enrollments.json" "student_progress.json" "tax_documents.json")
                ;;
            *)
                echo -e "${RED}Unknown persona: $persona${NC}"
                return 1
                ;;
        esac
    fi
    
    # Download each file
    local downloaded=0
    local total=${#files[@]}
    
    for file in "${files[@]}"; do
        local file_url="$REPO_URL/$persona/$file"
        echo -n "  Downloading $file... "
        
        if curl -s "$file_url" -o "$output_dir/$file"; then
            local size=$(ls -lh "$output_dir/$file" | awk '{print $5}')
            echo -e "${GREEN}✓${NC} ($size)"
            ((downloaded++))
        else
            echo -e "${RED}✗${NC}"
        fi
    done
    
    echo ""
    echo -e "${GREEN}Downloaded $downloaded/$total files to $output_dir${NC}"
    
    # Show summary
    if [ -f "$output_dir/manifest.json" ] && command -v jq >/dev/null 2>&1; then
        echo ""
        echo -e "${YELLOW}Dataset Summary:${NC}"
        jq -r '"  Name: " + .name, "  Description: " + .description, "  Business Model: " + .business_model' "$output_dir/manifest.json"
        
        if jq -e '.summary.note' "$output_dir/manifest.json" >/dev/null; then
            echo ""
            echo -e "${YELLOW}Note:${NC}"
            jq -r '"  " + .summary.note' "$output_dir/manifest.json"
        fi
    fi
    
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "  1. Explore the data: ls -la $output_dir/"
    echo "  2. Read the manifest: cat $output_dir/manifest.json"
    echo "  3. Start prototyping with your data!"
}

# Main logic
case "${1:-}" in
    --help|help|-h)
        show_help
        ;;
    --list|list)
        list_personas
        ;;
    --list-files)
        if [ -z "$2" ]; then
            echo -e "${RED}Please specify a persona${NC}"
            echo "Usage: ./tools/get-data.sh --list-files <persona>"
            exit 1
        fi
        list_files "$2"
        ;;
    "")
        echo -e "${RED}Please specify a persona${NC}"
        echo ""
        show_help
        exit 1
        ;;
    *)
        if [ "$2" = "--list-files" ]; then
            list_files "$1"
        else
            download_persona "$1" "$2"
        fi
        ;;
esac
