import { getTemporaryData } from "../../../../utils/temporaryLocaleStorage.js";

export function canvasSetup() {
  const data = getTemporaryData("localeGameData");
  if (!data) {
    window.location.hash = "games/locale";
    return;
  }
  const { users, ballSpeed, paddleHeight, winScore } = data;
  const canvas = document.querySelector("#gameCanvas");
  const ctx = canvas.getContext("2d");

  userSettings(users);
  createField(ctx, canvas);
  createPaddle(ctx, canvas, paddleHeight);
  createBall(ctx, canvas);
}

export function userSettings(users) {
  const user1Name = document.querySelector("#player1username");
  const user2Name = document.querySelector("#player2username");
  user1Name.textContent = users[0];
  user2Name.textContent = users[1];
}

export function createField(ctx, canvas) {
  ctx.setLineDash([5, 5]);
  ctx.beginPath();
  ctx.moveTo(canvas.width / 2, 0);
  ctx.lineTo(canvas.width / 2, canvas.height);
  ctx.strokeStyle = "white";
  ctx.stroke();
}

export function createPaddle(ctx, canvas, paddleHeight) {
  const paddleWidth = 10;
  let paddleY = canvas.height / 2 - paddleHeight / 2;
  ctx.fillStyle = "#60A5FA";
  ctx.fillRect(0, paddleY, paddleWidth, paddleHeight);
  ctx.fillRect(canvas.width - paddleWidth, paddleY, paddleWidth, paddleHeight);
}

export function createBall(ctx, canvas) {
  const ballX = canvas.width / 2;
  const ballY = canvas.height / 2;
  const ballSize = 10;
  ctx.fillStyle = "#F87171";
  ctx.beginPath();
  ctx.arc(ballX, ballY, ballSize, 0, Math.PI * 2);
  ctx.fill();
}

// -------------------------
// Pong game JavaScript
let gameStarted = false;
let leftScore = 0;
let rightScore = 0;
const canvas = document.getElementById("pong");
const context = canvas.getContext("2d");

const paddleWidth = 10;
const paddleHeight = 100;
const ballSize = 10;

const rightPaddle = {
  x: canvas.width - paddleWidth - 20,
  y: canvas.height / 2 - paddleHeight / 2,
  dy: 0,
};

const leftPaddle = {
  x: 20,
  y: canvas.height / 2 - paddleHeight / 2,
  dy: 0,
};

const ball = {
  x: canvas.width / 2,
  y: canvas.height / 2,
  radius: ballSize,
  speedX: 5,
  speedY: 5,
};

const paddleSpeed = 5;
const ballSpeed = 5;
let username = "";

// AI Paddle Movement with smooth tracking
function aiMove() {
  let aiSpeed = 3; // Speed of AI paddle movement, can adjust for difficulty

  // AI smooth paddle movement towards the ball's Y position
  if (ball.y < rightPaddle.y + paddleHeight / 2) {
    rightPaddle.dy = -aiSpeed;
  } else if (ball.y > rightPaddle.y + paddleHeight / 2) {
    rightPaddle.dy = aiSpeed;
  } else {
    rightPaddle.dy = 0;
  }

  // Smoothing: AI won't be overly fast, maintaining easier difficulty
  if (rightPaddle.y < 0) rightPaddle.y = 0;
  if (rightPaddle.y + paddleHeight > canvas.height)
    rightPaddle.y = canvas.height - paddleHeight;
}

function update() {
  if (!gameStarted) return;

  leftPaddle.y += leftPaddle.dy;
  if (leftPaddle.y < 0) leftPaddle.y = 0;
  if (leftPaddle.y + paddleHeight > canvas.height)
    leftPaddle.y = canvas.height - paddleHeight;

  // aiMove(); // AI paddle movement
  rightPaddle.y += rightPaddle.dy;

  ball.x += ball.speedX;
  ball.y += ball.speedY;

  if (ball.y - ball.radius <= 0 || ball.y + ball.radius >= canvas.height) {
    ball.speedY = -ball.speedY;
  }

  // Ball collision with paddles
  if (
    ball.x - ball.radius <= leftPaddle.x + paddleWidth &&
    ball.y > leftPaddle.y &&
    ball.y < leftPaddle.y + paddleHeight
  ) {
    ball.speedX = -ball.speedX;
  }

  if (
    ball.x + ball.radius >= rightPaddle.x &&
    ball.y > rightPaddle.y &&
    ball.y < rightPaddle.y + paddleHeight
  ) {
    ball.speedX = -ball.speedX;
  }

  // Scoring system: Ball goes out on left or right side
  if (ball.x - ball.radius <= 0) {
    rightScore++;
    resetBall();
  }

  if (ball.x + ball.radius >= canvas.width) {
    leftScore++;
    resetBall();
  }

  context.clearRect(0, 0, canvas.width, canvas.height);

  drawBall();
  drawPaddles();
  drawScores();
  drawUsername();

  requestAnimationFrame(update);
}

function drawPaddles() {
  context.fillStyle = "#FFFFFF";
  context.fillRect(leftPaddle.x, leftPaddle.y, paddleWidth, paddleHeight);
  context.fillRect(rightPaddle.x, rightPaddle.y, paddleWidth, paddleHeight);
}

function drawBall() {
  context.beginPath();
  context.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
  context.fillStyle = "#FFFFFF";
  context.fill();
  context.closePath();
}

function drawScores() {
  document.getElementById("score-left").textContent = leftScore;
  document.getElementById("score-right").textContent = rightScore;
}

function drawUsername() {
  document.getElementById("username_display").textContent =
    "Kullanıcı: " + username;
}

function resetBall() {
  ball.x = canvas.width / 2;
  ball.y = canvas.height / 2;
  ball.speedX = ballSpeed * (Math.random() < 0.5 ? 1 : -1);
  ball.speedY = ballSpeed * (Math.random() < 0.5 ? 1 : -1);
}

function startGame() {
  if (!gameStarted) {
    username = document.getElementById("username_log").value;
    document.getElementById("startButton").style.display = "none";
    document.getElementById("username_display").style.display = "block";
    gameStarted = true;
    update();
  }
}

document.addEventListener("keydown", function (event) {
  if (event.key === "w") leftPaddle.dy = -paddleSpeed;
  if (event.key === "s") leftPaddle.dy = paddleSpeed;
  if (event.key === "ArrowUp") rightPaddle.dy = -paddleSpeed;
  if (event.key === "ArrowDown") rightPaddle.dy = paddleSpeed;
});

document.addEventListener("keyup", function (event) {
  if (event.key === "w" || event.key === "s") leftPaddle.dy = 0;
  if (event.key === "ArrowUp" || event.key === "ArrowDown") rightPaddle.dy = 0;
});
