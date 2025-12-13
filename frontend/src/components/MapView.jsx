// src/components/MapView.jsx

import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

export default function MapView({ routeCoords, shipPosition }) {
  const mapContainer = useRef(null);
  const mapRef = useRef(null);
  const shipMarkerRef = useRef(null);

  /* ---------- INIT MAP ---------- */
  useEffect(() => {
    if (mapRef.current) return;

    mapRef.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://demotiles.maplibre.org/style.json",
      center: [70, 10],
      zoom: 4,
    });

    mapRef.current.addControl(new maplibregl.NavigationControl());
  }, []);

  /* ---------- DRAW / UPDATE ROUTE ---------- */
  useEffect(() => {
    if (!mapRef.current || routeCoords.length === 0) return;

    const geojson = {
      type: "Feature",
      geometry: {
        type: "LineString",
        coordinates: routeCoords.map(([lat, lon]) => [lon, lat]),
      },
    };

    if (mapRef.current.getSource("route")) {
      mapRef.current.getSource("route").setData(geojson);
      return;
    }

    mapRef.current.addSource("route", {
      type: "geojson",
      data: geojson,
    });

    mapRef.current.addLayer({
      id: "route-line",
      type: "line",
      source: "route",
      paint: {
        "line-color": "#FFD700",
        "line-width": 4,
      },
    });
  }, [routeCoords]);

  /* ---------- SHIP MARKER ---------- */
  useEffect(() => {
    if (!mapRef.current || !shipPosition) return;

    const { lat, lon } = shipPosition;

    if (!shipMarkerRef.current) {
      shipMarkerRef.current = new maplibregl.Marker({ color: "#00FFFF" })
        .setLngLat([lon, lat])
        .addTo(mapRef.current);
    } else {
      shipMarkerRef.current.setLngLat([lon, lat]);
    }
  }, [shipPosition]);

  return (
    <div
      ref={mapContainer}
      style={{ width: "100%", height: "100vh" }}
    />
  );
}
