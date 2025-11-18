#!/bin/bash
# Test script for Task 1.2: Install nginx in Docker Image
# This script validates that nginx is properly installed in the Docker image

set -e

echo "=== Test 1.2: nginx Installation Tests ==="
echo ""

# Colour codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Colour

# Test counter
PASSED=0
FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo -n "Testing: ${test_name}... "

    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Command: $test_command"
        ((FAILED++))
    fi
}

# Test 1: Docker image builds successfully
echo "Test 1: Building Docker image"
if docker build -f docker/Dockerfile -t mkdocs-nginx:test . > /tmp/docker_build.log 2>&1; then
    echo -e "${GREEN}PASS${NC} - Image built successfully"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC} - Image build failed"
    echo "Build log:"
    cat /tmp/docker_build.log
    ((FAILED++))
    exit 1
fi
echo ""

# Test 2: nginx binary exists and shows version
run_test "nginx version command" \
    "docker run --rm mkdocs-nginx:test nginx -v 2>&1 | grep -q 'nginx version'"

# Test 3: nginx binary is in PATH
run_test "nginx in PATH" \
    "docker run --rm mkdocs-nginx:test which nginx | grep -q '/nginx'"

# Test 4: nginx binary is executable
run_test "nginx is executable" \
    "docker run --rm mkdocs-nginx:test sh -c '[ -x \$(which nginx) ]'"

# Test 5: nginx can show help
run_test "nginx help command" \
    "docker run --rm mkdocs-nginx:test nginx -h 2>&1 | grep -q 'Usage: nginx'"

echo ""
echo "=== Test Summary ==="
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo ""

if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Tests FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}All tests PASSED${NC}"
    exit 0
fi
