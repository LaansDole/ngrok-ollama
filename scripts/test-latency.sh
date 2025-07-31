#!/bin/bash

# ngrok Latency Testing Script
# Tests the latency impact of ngrok tunneling on Ollama API calls
# Usage: ./test-latency.sh [ngrok-url] [iterations]

set -e

# Configuration
NGROK_URL="${1:-https://your-domain.ngrok.app}"
LOCAL_URL="http://localhost:11434"
ITERATIONS="${2:-10}"
TEST_ENDPOINT="/api/version"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 ngrok Latency Testing Tool${NC}"
echo -e "${BLUE}=================================${NC}"
echo ""
echo -e "Testing latency between:"
echo -e "  ${GREEN}Local:${NC}  $LOCAL_URL"
echo -e "  ${GREEN}ngrok:${NC}  $NGROK_URL"
echo -e "  ${GREEN}Iterations:${NC} $ITERATIONS"
echo ""

# Check if Ollama is running locally
echo -e "${YELLOW}⏳ Checking local Ollama server...${NC}"
if ! curl -s "$LOCAL_URL$TEST_ENDPOINT" > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Local Ollama server not responding at $LOCAL_URL${NC}"
    echo -e "   Please start Ollama with: ${BLUE}OLLAMA_HOST=0.0.0.0 ollama serve${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Local Ollama server is running${NC}"

# Check if ngrok tunnel is accessible
echo -e "${YELLOW}⏳ Checking ngrok tunnel...${NC}"
if ! curl -s "$NGROK_URL$TEST_ENDPOINT" > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: ngrok tunnel not responding at $NGROK_URL${NC}"
    echo -e "   Please start ngrok with: ${BLUE}make run${NC}"
    exit 1
fi
echo -e "${GREEN}✅ ngrok tunnel is accessible${NC}"
echo ""

# Function to measure latency
measure_latency() {
    local url=$1
    local name=$2
    local total_time=0
    local successful_requests=0
    local failed_requests=0
    
    echo -e "${YELLOW}📊 Testing $name latency...${NC}"
    
    for i in $(seq 1 $ITERATIONS); do
        # Measure time with curl
        start_time=$(date +%s%3N)
        if curl -s -o /dev/null "$url$TEST_ENDPOINT" 2>/dev/null; then
            end_time=$(date +%s%3N)
            latency=$((end_time - start_time))
            total_time=$((total_time + latency))
            successful_requests=$((successful_requests + 1))
            echo -e "  Request $i: ${latency}ms"
        else
            failed_requests=$((failed_requests + 1))
            echo -e "  Request $i: ${RED}FAILED${NC}"
        fi
        
        # Small delay between requests
        sleep 0.1
    done
    
    if [ $successful_requests -gt 0 ]; then
        local avg_latency=$((total_time / successful_requests))
        echo -e "  ${GREEN}Average: ${avg_latency}ms${NC}"
        echo -e "  ${GREEN}Success rate: $successful_requests/$ITERATIONS${NC}"
        echo $avg_latency
    else
        echo -e "  ${RED}All requests failed${NC}"
        echo "0"
    fi
    echo ""
}

# Run latency tests
echo -e "${BLUE}🚀 Starting latency measurements...${NC}"
echo ""

# Test local connection
local_latency=$(measure_latency "$LOCAL_URL" "Local")

# Test ngrok connection
ngrok_latency=$(measure_latency "$NGROK_URL" "ngrok")

# Calculate overhead
if [ "$local_latency" -gt 0 ] && [ "$ngrok_latency" -gt 0 ]; then
    overhead=$((ngrok_latency - local_latency))
    overhead_percent=$(echo "scale=1; ($overhead * 100) / $local_latency" | bc -l 2>/dev/null || echo "N/A")
    
    echo -e "${BLUE}📋 Results Summary${NC}"
    echo -e "${BLUE}=================${NC}"
    echo -e "Local average latency:    ${GREEN}${local_latency}ms${NC}"
    echo -e "ngrok average latency:    ${GREEN}${ngrok_latency}ms${NC}"
    echo -e "ngrok overhead:           ${YELLOW}+${overhead}ms${NC}"
    if [ "$overhead_percent" != "N/A" ]; then
        echo -e "Overhead percentage:      ${YELLOW}+${overhead_percent}%${NC}"
    fi
    echo ""
    
    # Performance assessment
    if [ "$overhead" -lt 50 ]; then
        echo -e "${GREEN}✅ Excellent performance - overhead < 50ms${NC}"
    elif [ "$overhead" -lt 100 ]; then
        echo -e "${YELLOW}⚠️  Good performance - overhead < 100ms${NC}"
    elif [ "$overhead" -lt 200 ]; then
        echo -e "${YELLOW}⚠️  Acceptable performance - overhead < 200ms${NC}"
    else
        echo -e "${RED}❌ Poor performance - overhead > 200ms${NC}"
        echo -e "   Consider optimizing ngrok configuration or using alternatives"
    fi
    echo ""
    
    # Recommendations
    echo -e "${BLUE}💡 Recommendations${NC}"
    echo -e "${BLUE}=================${NC}"
    if [ "$overhead" -gt 100 ]; then
        echo -e "• Consider using ngrok's regional endpoints closer to your location"
        echo -e "• Upgrade to a paid ngrok plan for better routing"
        echo -e "• Simplify your traffic policy configuration"
    fi
    echo -e "• Monitor latency regularly during development"
    echo -e "• Consider alternatives for production deployment if latency is critical"
    echo -e "• See docs/ngrok-latency-guide.md for detailed optimization guide"
    
else
    echo -e "${RED}❌ Could not calculate overhead due to test failures${NC}"
fi

echo ""
echo -e "${BLUE}📁 For optimization tips and alternatives, see:${NC}"
echo -e "   • docs/ngrok-latency-guide.md"
