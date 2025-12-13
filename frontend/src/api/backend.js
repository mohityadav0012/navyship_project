const BASE_URL = "http://127.0.0.1:8000";

/* ---------- STATIC ROUTE ---------- */
export async function fetchRoute(startLat, startLon, endLat, endLon) {
    const response = await fetch(`${BASE_URL}/route`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            start_lat: startLat,
            start_lon: startLon,
            end_lat: endLat,
            end_lon: endLon,
        }),
    });

    if (!response.ok) {
        throw new Error("Failed to fetch route");
    }

    return response.json();
}

/* ---------- STREAMING NAVIGATION (SSE) ---------- */
export function startNavigationStream(
    startLat,
    startLon,
    endLat,
    endLon,
    onEvent
) {
    const url =
        `${BASE_URL}/navigate_stream` +
        `?start_lat=${startLat}` +
        `&start_lon=${startLon}` +
        `&end_lat=${endLat}` +
        `&end_lon=${endLon}`;

    const evtSource = new EventSource(url);

    evtSource.addEventListener("init", e => onEvent("init", JSON.parse(e.data)));
    evtSource.addEventListener("update", e => onEvent("update", JSON.parse(e.data)));
    evtSource.addEventListener("reroute", e => onEvent("reroute", JSON.parse(e.data)));
    evtSource.addEventListener("reroute_success", e => onEvent("reroute_success", JSON.parse(e.data)));
    evtSource.addEventListener("done", e => {
        onEvent("done", JSON.parse(e.data));
        evtSource.close();
    });

    evtSource.onerror = () => {
        console.error("Streaming error");
        evtSource.close();
    };

    return evtSource;
}
