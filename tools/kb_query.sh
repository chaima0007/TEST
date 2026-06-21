#!/usr/bin/env bash
# Usage: KB_TOKEN=xxx KB_BASE=http://localhost:8080/v1 ./tools/kb_query.sh
KB_BASE="${KB_BASE:-https://kb.caelumpartners.eu/v1}"
KB_TOKEN="${KB_TOKEN:-changeme}"

echo "=== Health ==="
curl -sS "$KB_BASE/kb/health" | python3 -m json.tool

echo ""
echo "=== Search: CCO automobile LkSG (type=company, limit=3) ==="
curl -sS -H "Authorization: Bearer $KB_TOKEN" -H "Accept: application/json" \
  "$KB_BASE/kb/search?q=CCO%20automobile%20LkSG&type=company&limit=3" | python3 -m json.tool

echo ""
echo "=== Search: compliance officer ESG (all types) ==="
curl -sS -H "Authorization: Bearer $KB_TOKEN" -H "Accept: application/json" \
  "$KB_BASE/kb/search?q=compliance+officer&limit=5" | python3 -m json.tool

echo ""
echo "=== Company: volkswagen-group ==="
curl -sS -H "Authorization: Bearer $KB_TOKEN" \
  "$KB_BASE/kb/companies/volkswagen-group" | python3 -m json.tool
