#!/bin/bash
# Memory Game Test Script
# This script tests the basic functionality of the memory game

echo "========================================="
echo "Memory Game - Functional Test"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Start the server in background
echo "Starting memory game server..."
node memory-game.js > /tmp/test-memory-game.log 2>&1 &
SERVER_PID=$!
sleep 2

# Check if server is running
if ps -p $SERVER_PID > /dev/null; then
    print_result 0 "Server started successfully (PID: $SERVER_PID)"
else
    print_result 1 "Server failed to start"
    exit 1
fi

echo ""
echo "Testing API endpoints..."
echo ""

# Test 1: Homepage loads
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/)
if [ "$HTTP_CODE" = "200" ]; then
    print_result 0 "Homepage returns 200 OK"
else
    print_result 1 "Homepage returned HTTP $HTTP_CODE (expected 200)"
fi

# Test 2: CSS file loads
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/static/css/memory-game.css)
if [ "$HTTP_CODE" = "200" ]; then
    print_result 0 "CSS file loads successfully"
else
    print_result 1 "CSS file returned HTTP $HTTP_CODE (expected 200)"
fi

# Test 3: JS file loads
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/static/js/memory-game.js)
if [ "$HTTP_CODE" = "200" ]; then
    print_result 0 "JavaScript file loads successfully"
else
    print_result 1 "JavaScript file returned HTTP $HTTP_CODE (expected 200)"
fi

# Test 4: Stats API endpoint
STATS=$(curl -s http://localhost:3000/api/stats)
if echo "$STATS" | grep -q "gamesPlayed"; then
    print_result 0 "Stats API returns valid JSON"
else
    print_result 1 "Stats API did not return valid JSON"
fi

# Test 5: Game completion API
RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
    -d '{"moves": 15}' \
    http://localhost:3000/api/game-complete)
if echo "$RESPONSE" | grep -q "success"; then
    print_result 0 "Game completion API accepts POST requests"
else
    print_result 1 "Game completion API failed"
fi

# Test 6: Stats updated after game completion
STATS=$(curl -s http://localhost:3000/api/stats)
if echo "$STATS" | grep -q '"gamesPlayed":1'; then
    print_result 0 "Game statistics updated correctly"
else
    print_result 1 "Game statistics not updated"
fi

# Test 7: Best score tracking
if echo "$STATS" | grep -q '"bestScore":15'; then
    print_result 0 "Best score tracked correctly"
else
    print_result 1 "Best score not tracked correctly"
fi

# Test 8: HTML contains game elements
HTML=$(curl -s http://localhost:3000/)
if echo "$HTML" | grep -q "Memory Card Game"; then
    print_result 0 "HTML contains game title"
else
    print_result 1 "HTML missing game title"
fi

# Test 9: 404 for non-existent files
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/nonexistent.html)
if [ "$HTTP_CODE" = "404" ]; then
    print_result 0 "Returns 404 for non-existent files"
else
    print_result 1 "Did not return 404 for non-existent file (got $HTTP_CODE)"
fi

# Clean up - stop the server
echo ""
echo "Stopping server..."
kill $SERVER_PID 2>/dev/null
sleep 1
# Force kill if still running
if ps -p $SERVER_PID > /dev/null 2>&1; then
    kill -9 $SERVER_PID 2>/dev/null
fi

# Print summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi
