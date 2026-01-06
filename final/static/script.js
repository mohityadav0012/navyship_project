const canvas = document.getElementById('mapCanvas');
const ctx = canvas.getContext('2d');
const gridSize = 60; // Logical grid size (matches backend default sort of, but let's send this to backend)
const cellSize = canvas.width / gridSize;

let currentTool = 'land';
let isDrawing = false;

// State
let landGrid = Array(gridSize).fill().map(() => Array(gridSize).fill(0)); // 0: water, 1: land
let hazardGrid = Array(gridSize).fill().map(() => Array(gridSize).fill(0)); // 0: safe, 1: hazard
let startPoint = null; // {r, c}
let endPoint = null;   // {r, c}
let routes = {}; // { 'fastest': [[c, r], ...], ... }

// Elements
const calculateBtn = document.getElementById('calculateBtn');
const clearBtn = document.getElementById('clearBtn');
const toolBtns = document.querySelectorAll('.tool-btn');
const demoSelect = document.getElementById('demoSelect');
const loadDemoBtn = document.getElementById('loadDemoBtn');

// Tool Selection
toolBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelector('.tool-btn.active').classList.remove('active');
        btn.classList.add('active');
        currentTool = btn.dataset.tool;
    });
});

// Canvas Interaction
canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;
    handleCanvasClick(e);
});
canvas.addEventListener('mousemove', (e) => {
    if (isDrawing && (currentTool === 'land' || currentTool === 'hazard' || currentTool === 'eraser')) {
        handleCanvasClick(e);
    }
});
canvas.addEventListener('mouseup', () => isDrawing = false);
canvas.addEventListener('mouseleave', () => isDrawing = false);

function getGridPos(e) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const c = Math.floor(x / cellSize);
    const r = Math.floor(y / cellSize);
    return { r, c };
}

function handleCanvasClick(e) {
    const { r, c } = getGridPos(e);
    if (r < 0 || r >= gridSize || c < 0 || c >= gridSize) return;

    if (currentTool === 'land') {
        landGrid[r][c] = 1;
        hazardGrid[r][c] = 0; // Clear hazard if land (mutually exclusive visually mostly)
    } else if (currentTool === 'hazard') {
        hazardGrid[r][c] = 1;
        landGrid[r][c] = 0; // Clear land if hazard (usually water hazard)
    } else if (currentTool === 'eraser') {
        landGrid[r][c] = 0;
        hazardGrid[r][c] = 0;
    } else if (currentTool === 'start') {
        startPoint = { r, c };
    } else if (currentTool === 'end') {
        endPoint = { r, c };
    }
    draw();
}

// Drawing Logic
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw Land and Hazards
    for (let r = 0; r < gridSize; r++) {
        for (let c = 0; c < gridSize; c++) {
            if (landGrid[r][c] === 1) {
                ctx.fillStyle = '#64748b'; // Slate 500
                ctx.fillRect(c * cellSize, r * cellSize, cellSize, cellSize);
            } else if (hazardGrid[r][c] === 1) {
                ctx.fillStyle = 'rgba(239, 68, 68, 0.4)'; // Red 500 transparent
                ctx.fillRect(c * cellSize, r * cellSize, cellSize, cellSize);
            }
        }
    }

    // Draw Routes
    if (routes['coastal']) drawPath(routes['coastal'], '#f97316'); // Orange
    if (routes['fuel_efficient']) drawPath(routes['fuel_efficient'], '#22c55e'); // Green
    if (routes['fastest']) drawPath(routes['fastest'], '#38bdf8'); // Blue (changed for contrast with red hazard)

    // Draw Points
    if (startPoint) {
        ctx.fillStyle = '#4ade80'; // Bright Green
        ctx.beginPath();
        ctx.arc((startPoint.c + 0.5) * cellSize, (startPoint.r + 0.5) * cellSize, cellSize * 1.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.stroke();
    }
    if (endPoint) {
        ctx.fillStyle = '#f87171'; // Red
        ctx.beginPath();
        ctx.arc((endPoint.c + 0.5) * cellSize, (endPoint.r + 0.5) * cellSize, cellSize * 1.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#000';
        ctx.stroke();
    }
}

function drawPath(path, color) {
    if (!path || path.length === 0) return;
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.moveTo((path[0][0] + 0.5) * cellSize, (path[0][1] + 0.5) * cellSize);
    for (let i = 1; i < path.length; i++) {
        ctx.lineTo((path[i][0] + 0.5) * cellSize, (path[i][1] + 0.5) * cellSize);
    }
    ctx.stroke();
}

// Actions
calculateBtn.addEventListener('click', async () => {
    if (!startPoint || !endPoint) {
        alert("Please set both Start and End points.");
        return;
    }

    calculateBtn.textContent = "Calculating...";

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                width: gridSize,
                height: gridSize,
                start: [startPoint.r, startPoint.c],
                end: [endPoint.r, endPoint.c],
                landGrid: landGrid,
                hazardGrid: hazardGrid
            })
        });

        const data = await response.json();
        routes = data;
        draw();
    } catch (err) {
        console.error(err);
        alert("Error calculating routes.");
    } finally {
        calculateBtn.textContent = "Calculate Routes";
    }
});

clearBtn.addEventListener('click', () => {
    landGrid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
    hazardGrid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
    startPoint = null;
    endPoint = null;
    routes = {};
    draw();
});

// Demo Loading
async function fetchDemos() {
    try {
        const res = await fetch('/demos');
        const demos = await res.json();
        demos.forEach(demo => {
            const option = document.createElement('option');
            option.value = demo.id;
            option.textContent = demo.name;
            demoSelect.appendChild(option);
        });
    } catch (e) {
        console.error("Failed to fetch demos", e);
    }
}

loadDemoBtn.addEventListener('click', async () => {
    const id = demoSelect.value;
    if (!id) return;

    try {
        const res = await fetch(`/load_demo/${id}`);
        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // Reset and Load
        landGrid = data.landGrid;
        hazardGrid = data.hazardGrid || Array(gridSize).fill().map(() => Array(gridSize).fill(0));
        startPoint = { r: data.start[0], c: data.start[1] };
        endPoint = { r: data.end[0], c: data.end[1] };
        routes = {};

        draw();
    } catch (e) {
        console.error("Failed to load demo", e);
    }
});

// Initial draw & fetch
draw();
fetchDemos();
