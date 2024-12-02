import {
  getTemporaryData,
  removeTemporaryData,
} from "../../../../utils/temporaryLocaleStorage.js";

export class AiGame {
  #canvas = document.getElementById("gameCanvas");
  #ctx = this.#canvas.getContext("2d");
  #data;
  constructor() {
    this.#data = getTemporaryData("aiGameData");
    if (!this.#data) {
      window.location.hash = "games/ai";
      return;
    }
    console.log(this.#gameSettings);
    console.log(this.#data);
    this.#player1 = {
      name: this.#data.users[0],
      score: 0,
    };
    this.#aiPlayer = {
      name: "MOULINETTE",
      score: 0,
    };
    this.#gameSettings = {
      ...this.#gameSettings,
      ballSpeed: parseInt(this.#data.ballSpeed, 10),
      paddleHeight: parseInt(this.#data.paddleHeight, 10),
      paddleSpeed: parseInt(this.#data.ballSpeed, 10) * 1.5,
      winScore: parseInt(this.#data.winScore, 10),
      aiSpeedMultiplier: parseInt(this.#data.gameDifficulty, 10),
    };

    this.#setBallSpeed();
    this.#setAiDifficulty();

    this.#startGame();
  }
  #player1 = { name: "Player 1", score: 0 };
  #aiPlayer = { name: "MOULINETTE", score: 0 };
  #gameSettings = {
    ballSpeed: 1,
    ballSize: 10,
    paddleHeight: 100,
    paddleWidth: 10,
    paddleSpeed: 1.5,
    winScore: 5,
    aiSpeedMultiplier: 1,
  };
  #isGameStarted = false;
  #ball = {
    x: this.#canvas.width / 2,
    y: this.#canvas.height / 2,
    radius: this.#gameSettings.ballSize,
    speedX: this.#gameSettings.ballSpeed,
    speedY: this.#gameSettings.ballSpeed,
  };
  #playerPaddle = {
    x: 0,
    y: this.#canvas.height / 2 - this.#gameSettings.paddleHeight / 2,
    dy: 0,
  };
  #aiPaddle = {
    x: this.#canvas.width - this.#gameSettings.paddleWidth,
    y: this.#canvas.height / 2 - this.#gameSettings.paddleHeight / 2,
    dy: this.#ball.speedY * this.#gameSettings.aiSpeedMultiplier,
  };

  #setBallSpeed() {
    this.#ball.speedX = this.#gameSettings.ballSpeed;
    this.#ball.speedY = this.#gameSettings.ballSpeed;
  }

  #setAiDifficulty() {
    switch (this.#gameSettings.aiSpeedMultiplier) {
      case 1:
        this.#aiPaddle.dy = this.#ball.speedY * 0.01;
        break;
      case 2:
        this.#aiPaddle.dy = this.#ball.speedY * 0.05;
        break;
      case 3:
        this.#aiPaddle.dy = this.#ball.speedY * 0.1;
        break;
      case 4:
        this.#aiPaddle.dy = this.#ball.speedY * 0.5;
        break;
      default:
        this.#aiPaddle.dy = this.#ball.speedY * 1;
        break;
    }
  }

  #startGame() {
    if (this.#isGameStarted) return;
    this.#isGameStarted = true;

    document.addEventListener("keydown", (event) => {
      if (event.key === "w")
        this.#playerPaddle.dy = -this.#gameSettings.paddleSpeed;
      if (event.key === "s")
        this.#playerPaddle.dy = this.#gameSettings.paddleSpeed;
    });

    document.addEventListener("keyup", (event) => {
      if (event.key === "w" || event.key === "s") this.#playerPaddle.dy = 0;
    });

    this.#userSettings();
    this.#update();
  }

  #update() {
    if (!this.#isGameStarted) return;

    // Update player paddle position
    this.#playerPaddle.y += this.#playerPaddle.dy;

    // Constrain player paddle within the canvas
    if (this.#playerPaddle.y < 0) this.#playerPaddle.y = 0;
    else if (
      this.#playerPaddle.y + this.#gameSettings.paddleHeight >
      this.#canvas.height
    )
      this.#playerPaddle.y =
        this.#canvas.height - this.#gameSettings.paddleHeight;

    // Update AI paddle position based on difficulty level
    this.#aiPaddle.y += (this.#ball.y - this.#aiPaddle.y) * this.#aiPaddle.dy;

    if (this.#aiPaddle.y < 0) this.#aiPaddle.y = 0;
    else if (
      this.#aiPaddle.y + this.#gameSettings.paddleHeight >
      this.#canvas.height
    )
      this.#aiPaddle.y = this.#canvas.height - this.#gameSettings.paddleHeight;

    // Update ball position
    this.#ball.x += this.#ball.speedX;
    this.#ball.y += this.#ball.speedY;

    // Ball collision with top and bottom walls
    if (
      this.#ball.y - this.#ball.radius <= 0 ||
      this.#ball.y + this.#ball.radius >= this.#canvas.height
    ) {
      this.#ball.speedY = -this.#ball.speedY;
    }

    // Ball collision with paddles
    if (
      this.#ball.x - this.#ball.radius <=
        this.#playerPaddle.x + this.#gameSettings.paddleWidth &&
      this.#ball.y > this.#playerPaddle.y &&
      this.#ball.y < this.#playerPaddle.y + this.#gameSettings.paddleHeight
    ) {
      this.#ball.speedX = -this.#ball.speedX;
    }

    if (
      this.#ball.x + this.#ball.radius >= this.#aiPaddle.x &&
      this.#ball.y > this.#aiPaddle.y &&
      this.#ball.y < this.#aiPaddle.y + this.#gameSettings.paddleHeight
    ) {
      this.#ball.speedX = -this.#ball.speedX;
    }

    // Scoring system
    if (this.#ball.x - this.#ball.radius <= 0) {
      this.#aiPlayer.score++;
      this.#updateScores();
      this.#resetBall();
    }

    if (this.#ball.x + this.#ball.radius >= this.#canvas.width) {
      this.#player1.score++;
      this.#updateScores();
      this.#resetBall();
    }

    // Clear canvas
    this.#ctx.clearRect(0, 0, this.#canvas.width, this.#canvas.height);

    // Draw game elements
    this.#drawPaddles();
    this.#createField();
    this.#createBall();

    requestAnimationFrame(this.#update.bind(this));
  }

  #drawPaddles() {
    this.#ctx.fillStyle = "#60A5FA";
    this.#ctx.fillRect(
      this.#playerPaddle.x,
      this.#playerPaddle.y,
      this.#gameSettings.paddleWidth,
      this.#gameSettings.paddleHeight
    );
    this.#ctx.fillRect(
      this.#aiPaddle.x,
      this.#aiPaddle.y,
      this.#gameSettings.paddleWidth,
      this.#gameSettings.paddleHeight
    );
  }

  #createBall() {
    this.#ctx.fillStyle = "#F87171";
    this.#ctx.beginPath();
    this.#ctx.arc(
      this.#ball.x,
      this.#ball.y,
      this.#ball.radius,
      0,
      Math.PI * 2
    );
    this.#ctx.fill();
  }

  #createField() {
    this.#ctx.setLineDash([5, 5]);
    this.#ctx.beginPath();
    this.#ctx.moveTo(this.#canvas.width / 2, 0);
    this.#ctx.lineTo(this.#canvas.width / 2, this.#canvas.height);
    this.#ctx.strokeStyle = "white";
    this.#ctx.stroke();
  }

  #resetBall() {
    this.#ball.x = this.#canvas.width / 2;
    this.#ball.y = this.#canvas.height / 2;
    this.#ball.speedX =
      this.#gameSettings.ballSpeed * (Math.random() < 0.5 ? 1 : -1);
    this.#ball.speedY =
      this.#gameSettings.ballSpeed * (Math.random() < 0.5 ? 1 : -1);
  }

  #userSettings() {
    document.querySelector("#player1username").innerText = this.#player1.name;
    document.querySelector("#aiusername").innerText = this.#aiPlayer.name;
  }

  #updateScores() {
    document.querySelector("#player1score").innerText = this.#player1.score;
    document.querySelector("#aiscore").innerText = this.#aiPlayer.score;
    if (this.#player1.score >= this.#gameSettings.winScore) {
      this.#isGameStarted = false;
      this.#gameOver(this.#player1.name);
    } else if (this.#aiPlayer.score >= this.#gameSettings.winScore) {
      this.#isGameStarted = false;
      this.#gameOver(this.#aiPlayer.name);
    }
  }

  #gameOver(winner) {
    removeTemporaryData("aiGameData");
    alert(`${winner} wins!`);
    window.location.hash = "games/ai";
  }
}
