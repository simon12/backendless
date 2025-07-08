document.addEventListener("DOMContentLoaded", function() {
  const canvas = document.getElementById("circleCanvas");
  const ctx = canvas.getContext("2d");
  const radiusSlider = document.getElementById("radiusSlider");
  const radiusValue = document.getElementById("radiusValue");
  const colorPicker = document.getElementById("colorPicker");
  const drawCircleBtn = document.getElementById("drawCircleBtn");
  const clearCanvasBtn = document.getElementById("clearCanvasBtn");
  
  // Set initial canvas background
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  // Update radius value display when slider changes
  radiusSlider.addEventListener("input", function() {
    radiusValue.textContent = this.value;
  });
  
  // Draw circle button click handler
  drawCircleBtn.addEventListener("click", function() {
    drawCircle();
  });
  
  // Clear canvas button click handler
  clearCanvasBtn.addEventListener("click", function() {
    clearCanvas();
  });
  
  // Allow clicking on canvas to draw circle at that position
  canvas.addEventListener("click", function(event) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    const x = (event.clientX - rect.left) * scaleX;
    const y = (event.clientY - rect.top) * scaleY;
    
    drawCircleAt(x, y);
  });
  
  // Function to draw circle at center of canvas
  function drawCircle() {
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = parseInt(radiusSlider.value);
    const color = colorPicker.value;
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 2;
    ctx.stroke();
  }
  
  // Function to draw circle at specific position
  function drawCircleAt(x, y) {
    const radius = parseInt(radiusSlider.value);
    const color = colorPicker.value;
    
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 2;
    ctx.stroke();
  }
  
  // Function to clear canvas
  function clearCanvas() {
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }
  
  // Draw initial circle
  drawCircle();
});

