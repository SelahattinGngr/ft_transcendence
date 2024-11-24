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
