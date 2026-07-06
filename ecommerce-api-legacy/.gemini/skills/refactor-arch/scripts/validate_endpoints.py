#!/usr/bin/env python3
"""Smoke-test common endpoints after refactoring."""
import json
import sys
import urllib.error
import urllib.request

DEFAULT_ENDPOINTS = ["/", "/health", "/produtos"]

def check(base_url: str, endpoints: list) -> bool:
    ok = True
    for ep in endpoints:
        url = base_url.rstrip("/") + ep
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                status = resp.status
                print(f"  OK {ep} -> {status}")
        except urllib.error.HTTPError as e:
            print(f"  HTTP {ep} -> {e.code}")
            if e.code >= 500:
                ok = False
        except Exception as e:
            print(f"  FAIL {ep} -> {e}")
            ok = False
    return ok

if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    eps = sys.argv[2:] if len(sys.argv) > 2 else DEFAULT_ENDPOINTS
    success = check(base, eps)
    sys.exit(0 if success else 1)
