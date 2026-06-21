#!/bin/bash
# Caelum Partners — Load Test Script
# Usage: ./tools/load_test.sh [BASE_URL] [CONCURRENCY] [REQUESTS]
#
# Requirements: apache2-utils (for ab) or curl (fallback)
# Install ab: sudo apt-get install apache2-utils (Ubuntu/Debian)
#             brew install httpd (macOS)

BASE_URL="${1:-http://localhost:3000}"
CONCURRENCY="${2:-10}"
REQUESTS="${3:-100}"

ENDPOINTS=(
  "/api/digital-gender-gap-rights-engine"
  "/api/land-grabbing-rights-engine"
  "/api/prison-labor-rights-engine"
  "/api/statelessness-rights-engine"
  "/api/algorithmic-bias-rights-engine"
)

echo "======================================================"
echo " Caelum Partners — Load Test"
echo " Base URL    : $BASE_URL"
echo " Concurrency : $CONCURRENCY"
echo " Requests    : $REQUESTS"
echo "======================================================"
echo ""

# Use ab (Apache Bench) if available, else curl loop
if command -v ab &> /dev/null; then
  echo "[ab] Apache Bench detected — running structured load test"
  echo ""
  for ep in "${ENDPOINTS[@]}"; do
    echo "------------------------------------------------------"
    echo "Load testing $ep..."
    ab -n "$REQUESTS" -c "$CONCURRENCY" "${BASE_URL}${ep}" 2>&1 | grep -E "Requests per second|Time per request|Failed requests|Non-2xx"
    echo ""
  done
else
  echo "[curl] ab not found — using curl loop (install apache2-utils for ab)"
  echo ""
  for ep in "${ENDPOINTS[@]}"; do
    echo "------------------------------------------------------"
    echo "Testing $ep (10 parallel requests)..."
    for i in $(seq 1 10); do
      curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" "${BASE_URL}${ep}" &
    done
    wait
    echo ""
  done
fi

echo "======================================================"
echo " Load test complete."
echo "======================================================"
