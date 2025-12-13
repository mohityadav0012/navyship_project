// src/App.jsx

import { useState } from "react";
import MapView from "./components/MapView";
import ControlPanel from "./components/ControlPanel";
import { startNavigationStream } from "./api/backend";

export default function App() {
  const [routeCoords, setRouteCoords] = useState([]);
  const [shipPosition, setShipPosition] = useState(null);
  const [eventSource, setEventSource] = useState(null);

  const startNavigation = (sLat, sLon, eLat, eLon) => {
    if (eventSource) eventSource.close();

    const es = startNavigationStream(
      sLat,
      sLon,
      eLat,
      eLon,
      (type, data) => {
        if (type === "init" || type === "reroute_success") {
          setRouteCoords(data.path_latlon);
        }

        if (type === "update") {
          setShipPosition(data.position);
        }

        if (type === "done") {
          console.log("Navigation completed");
        }
      }
    );

    setEventSource(es);
  };

  return (
    <>
      <ControlPanel onStart={startNavigation} />
      <MapView
        routeCoords={routeCoords}
        shipPosition={shipPosition}
      />
    </>
  );
}
