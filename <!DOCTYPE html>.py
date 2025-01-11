<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HOLOGON8 Quantum Study Calculator</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f9;
      color: #333;
      margin: 0;
      padding: 20px;
    }
    h1, h2 {
      text-align: center;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
    }
    .input-group, .button-group {
      margin-bottom: 15px;
    }
    label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
    }
    input, select, button {
      width: 100%;
      padding: 8px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
    button {
      background-color: #007bff;
      color: white;
      cursor: pointer;
    }
    button:hover {
      background-color: #0056b3;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    th, td {
      border: 1px solid #ccc;
      padding: 10px;
      text-align: center;
    }
    th {
      background-color: #007bff;
      color: white;
    }
    canvas {
      margin-top: 20px;
      display: block;
      width: 100%;
      height: 400px;
    }
    .error {
      color: red;
      font-size: 14px;
      margin-top: -10px;
      margin-bottom: 10px;
    }
  </style>
</head>
<body>
  <h1>HOLOGON8 Quantum Study Calculator</h1>
  <div class="container">
    <h2>Iterative Branching Sequence</h2>
    <div class="input-group">
      <label for="branchType">Branch Type:</label>
      <select id="branchType">
        <option value="linear">Linear</option>
        <option value="oscillatory">Oscillatory</option>
        <option value="exponential">Exponential</option>
      </select>
    </div>
    <div class="input-group">
      <label for="initialValue">Initial Value (x₀):</label>
      <input type="number" id="initialValue" value="0">
      <div class="error" id="initialValueError"></div>
    </div>
    <div class="input-group">
      <label for="branchFactor">Branching Factor (k):</label>
      <input type="number" id="branchFactor" value="0.02" step="0.01">
      <div class="error" id="branchFactorError"></div>
    </div>
    <div class="input-group">
      <label for="iterations">Number of Iterations (n):</label>
      <input type="number" id="iterations" value="50">
      <div class="error" id="iterationsError"></div>
    </div>
    <div class="button-group">
      <button id="calculateButton">Calculate</button>
    </div>
    <table>
      <thead>
        <tr>
          <th>Iteration (n)</th>
          <th>Value (fₙ)</th>
        </tr>
      </thead>
      <tbody id="resultsTable"></tbody>
    </table>
    <canvas id="resultsChart"></canvas>
    
    <h2>Branch Tree Visualization</h2>
    <div id="treeControls">
      <label for="treeLevels">Number of Levels:</label>
      <input type="number" id="treeLevels" value="5" min="1" max="10">
      <div class="error" id="treeLevelsError"></div>
      <button id="drawTreeButton">Draw Tree</button>
    </div>
    <canvas id="treeCanvas"></canvas>
    
    <h2>Symbolic Analysis</h2>
    <pre id="symbolicAnalysis"></pre>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    let chartInstance = null;

    function validateInputs() {
      let isValid = true;

      const initialValue = parseFloat(document.getElementById("initialValue").value);
      const branchFactor = parseFloat(document.getElementById("branchFactor").value);
      const iterations = parseInt(document.getElementById("iterations").value);

      const initialValueError = document.getElementById("initialValueError");
      const branchFactorError = document.getElementById("branchFactorError");
      const iterationsError = document.getElementById("iterationsError");

      initialValueError.textContent = "";
      branchFactorError.textContent = "";
      iterationsError.textContent = "";

      if (isNaN(initialValue)) {
        initialValueError.textContent = "Initial Value must be a number.";
        isValid = false;
      }

      if (isNaN(branchFactor) || branchFactor <= 0) {
        branchFactorError.textContent = "Branching Factor must be a positive number.";
        isValid = false;
      }

      if (isNaN(iterations) || iterations <= 0 || iterations > 100) {
        iterationsError.textContent = "Number of Iterations must be a positive number between 1 and 100.";
        isValid = false;
      }

      return isValid;
    }

    document.getElementById("calculateButton").addEventListener("click", () => {
      if (!validateInputs()) return;

      const branchType = document.getElementById("branchType").value;
      const initialValue = parseFloat(document.getElementById("initialValue").value);
      const branchFactor = parseFloat(document.getElementById("branchFactor").value);
      const iterations = parseInt(document.getElementById("iterations").value);

      const resultsTable = document.getElementById("resultsTable");
      resultsTable.innerHTML = "";

      const values = [];
      let currentValue = initialValue;

      for (let n = 0; n <= iterations; n++) {
        resultsTable.innerHTML += `<tr><td>${n}</td><td>${currentValue.toFixed(5)}</td></tr>`;
        values.push({ x: n, y: currentValue });

        if (branchType === 'linear') {
          currentValue += branchFactor * currentValue;
        } else if (branchType === 'oscillatory') {
          currentValue += branchFactor * Math.sin(currentValue);
        } else if (branchType === 'exponential') {
          currentValue += branchFactor * Math.pow(currentValue, 2);
        }
      }

      drawChart(values, "resultsChart");
    });

    function drawChart(data, canvasId) {
      const ctx = document.getElementById(canvasId).getContext("2d");

      if (chartInstance) chartInstance.destroy();

      chartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: data.map(point => point.x),
          datasets: [{
            label: "Branching Sequence",
            data: data.map(point => point.y),
            borderColor: "#007bff",
            borderWidth: 2,
            fill: false
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Iteration (n)"
              }
            },
            y: {
              title: {
                display: true,
                text: "Value (fₙ)"
              }
            }
          }
        }
      });
    }

    document.getElementById("drawTreeButton").addEventListener("click", () => {
      const levels = parseInt(document.getElementById("treeLevels").value);
      const treeLevelsError = document.getElementById("treeLevelsError");

      treeLevelsError.textContent = "";

      if (isNaN(levels) || levels < 1 || levels > 10) {
        treeLevelsError.textContent = "Tree Levels must be between 1 and 10.";
        return;
      }

      drawTree(0, levels, 0.02, "treeCanvas");
    });

    function drawTree(x, level, k, canvasId) {
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext("2d");
      canvas.width = canvas.clientWidth;
      canvas.height = canvas.clientHeight;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      