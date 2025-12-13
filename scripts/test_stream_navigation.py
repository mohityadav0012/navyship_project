import sseclient
import requests

url = "http://127.0.0.1:8000/navigate_stream"

payload = {
    "start_lat": 10.0,
    "start_lon": 70.0,
    "end_lat": 12.0,
    "end_lon": 75.0
}

# Make POST request (SSE requires streaming=True)
response = requests.post(url, json=payload, stream=True)

client = sseclient.SSEClient(response)

print("\n===== STREAMING STARTED =====\n")

for event in client.events():
    print(f"[{event.event}] {event.data}")

    if event.event == "done" or event.event == "error":
        print("\n===== STREAM ENDED =====")
        break
