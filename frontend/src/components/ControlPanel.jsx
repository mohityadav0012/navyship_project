// src/components/ControlPanel.jsx

import { useState } from "react";

export default function ControlPanel({ onStart }) {
  const [startLat, setStartLat] = useState(10.0);
  const [startLon, setStartLon] = useState(70.0);
  const [endLat, setEndLat] = useState(12.0);
  const [endLon, setEndLon] = useState(75.0);

  return (
    <div
      style={{
        position: "absolute",
        top: 20,
        left: 20,
        zIndex: 10,
        background: "white",
        padding: 15,
        borderRadius: 8,
        width: 240,
        boxShadow: "0 2px 10px rgba(0,0,0,0.2)",
      }}
    >
      <h3>Ship Navigation</h3>

      <label>Start Latitude</label>
      <input value={startLat} onChange={e => setStartLat(+e.target.value)} />

      <label>Start Longitude</label>
      <input value={startLon} onChange={e => setStartLon(+e.target.value)} />

      <label>End Latitude</label>
      <input value={endLat} onChange={e => setEndLat(+e.target.value)} />

      <label>End Longitude</label>
      <input value={endLon} onChange={e => setEndLon(+e.target.value)} />

      <button
        style={{ marginTop: 10, width: "100%" }}
        onClick={() =>
          onStart(startLat, startLon, endLat, endLon)
        }
      >
        Start Navigation
      </button>
    </div>
  );
}
