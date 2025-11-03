"""Test script for CE Email Summarizer API"""
import requests
import json

API_BASE = "http://localhost:8000"

# Sample thread data
test_thread = {
    "thread_id": "CE-405467-683",
    "topic": "Damaged product on arrival",
    "subject": "Order 405467-683: Damaged item received",
    "initiated_by": "customer",
    "order_id": "405467-683",
    "product": "LED Monitor",
    "messages": [
        {
            "id": "m1",
            "sender": "customer",
            "timestamp": "2025-09-12T06:39:29",
            "body": "Hello, my item arrived damaged. Order 405467-683 LED Monitor. Pending confirm photos question credit 7732 tracking broken packaging stock status order."
        },
        {
            "id": "m2",
            "sender": "company",
            "timestamp": "2025-09-12T06:49:29",
            "body": "Please decline 3206 stock when reroute delivery help 3580 summary size delayed warehouse address tomorrow credit today credit decline size please summary photos why policy."
        },
        {
            "id": "m3",
            "sender": "customer",
            "timestamp": "2025-09-12T06:59:29",
            "body": "Broken 2965 color 4739."
        }
    ]
}

print("🧪 Testing CE Email Summarizer API\n")

# Test health endpoint
print("1. Testing health endpoint...")
response = requests.get(f"{API_BASE}/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {json.dumps(response.json(), indent=2)}\n")

# Test summarization endpoint
print("2. Testing summarization endpoint...")
response = requests.post(
    f"{API_BASE}/api/summarize",
    json={"thread": test_thread}
)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"   Success: {result['success']}")
    print(f"\n   Summary Details:")
    summary = result['summary']
    print(f"   - Thread ID: {summary['thread_id']}")
    print(f"   - Category: {summary['issue_category']}")
    print(f"   - Sentiment: {summary['sentiment']}")
    print(f"   - Priority: {summary['priority']}")
    print(f"   - Status: {summary['status']}")
    print(f"   - Summary: {summary['summary']}")
    print(f"   - Action Items:")
    for item in summary['action_items']:
        print(f"     • {item}")
else:
    print(f"   Error: {response.text}")

print("\n✅ API test complete!")
