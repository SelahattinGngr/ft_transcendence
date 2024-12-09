import { getTemporaryData } from "../../../../utils/temporaryLocaleStorage.js";

export class Game {
  #canvas = document.getElementById("gameCanvas");
  #ctx = this.#canvas.getContext("2d");
  #data = getTemporaryData("tournamentGameData");
  constructor() {
    if (!this.#data) {
      console.error("Oyun verileri eksik!");
      return;
    }

    this.#player1 = {
      name: this.#data.users[0],
      score: 0,
    };
    this.#player2 = {
      name: this.#data.users[1],
      score: 0,
    };
    this.#startGame();
  }
  #onMatchEnd;
  #ballSpeed = parseInt(this.#data.ballSpeed, 10);
  #ballSize = 7.5;
  #paddleHeight = parseInt(this.#data.paddleHeight, 10) / 1.75;
  #paddleWidth = 10;
  #paddleSpeed = parseInt(this.#data.ballSpeed, 10) * 1.75;
  #winScore = parseInt(this.#data.winScore, 10);

  onMatchEnd(callback) {
    this.#onMatchEnd = callback;
  }

  #player1 = { name: "Player 1", score: 0 };
  #player2 = { name: "Player 2", score: 0 };
  #isGameStarted = false;
  #ball = {
    x: this.#canvas.width / 2,
    y: this.#canvas.height / 2,
    radius: this.#ballSize,
    speedX: this.#ballSpeed,
    speedY: this.#ballSpeed,
  };
  #leftPaddle = {
    x: 0,
    y: this.#canvas.height / 2 - this.#paddleHeight / 2,
    dy: 0,
  };
  #rightPaddle = {
    x: this.#canvas.width - this.#paddleWidth,
    y: this.#canvas.height / 2 - this.#paddleHeight / 2,
    dy: 0,
  };

  #startGame() {
    if (this.#isGameStarted) return;
    this.#isGameStarted = true;
    this.#startCountdown(5);
  }

  #startCountdown(seconds) {
    let remainingTime = seconds;
    const interval = setInterval(() => {
      this.#ctx.clearRect(0, 0, this.#canvas.width, this.#canvas.height);
      this.#ctx.fillStyle = "white";
      this.#ctx.font = "48px Arial";
      this.#ctx.textAlign = "center";
      this.#ctx.textBaseline = "middle";
      this.#ctx.fillText(
        remainingTime,
        this.#canvas.width / 2,
        this.#canvas.height / 2
      );

      if (remainingTime <= 0) {
        clearInterval(interval);
        this.#initializeGame();
      } else {
        remainingTime--;
      }
    }, 1000);
  }

  #keyboardList = ["w", "s", "ArrowUp", "ArrowDown"];
  #initializeGame() {
    document.addEventListener("keydown", (event) => {
      if (!this.#keyboardList.includes(event.key)) return;
      event.preventDefault();
      if (event.key === "w") this.#leftPaddle.dy = -this.#paddleSpeed;
      if (event.key === "s") this.#leftPaddle.dy = this.#paddleSpeed;
      if (event.key === "ArrowUp") this.#rightPaddle.dy = -this.#paddleSpeed;
      if (event.key === "ArrowDown") this.#rightPaddle.dy = this.#paddleSpeed;
    });

    document.addEventListener("keyup", (event) => {
      if (!this.#keyboardList.includes(event.key)) return;
      event.preventDefault();
      if (event.key === "w" || event.key === "s") this.#leftPaddle.dy = 0;
      if (event.key === "ArrowUp" || event.key === "ArrowDown")
        this.#rightPaddle.dy = 0;
    });

    this.#userSettings();
    this.#updateScores();
    this.#update();
  }

  #update() {
    if (!this.#isGameStarted) return;

    // Update paddle positions
    this.#leftPaddle.y += this.#leftPaddle.dy;
    this.#rightPaddle.y += this.#rightPaddle.dy;

    // Constrain paddles within the canvas
    this.#constrainPaddles();

    // Update ball position
    this.#updateBallPosition();

    // Check scoring
    this.#checkScoring();

    // Clear canvas and redraw elements
    this.#ctx.clearRect(0, 0, this.#canvas.width, this.#canvas.height);
    this.#drawField();
    this.#drawBall();
    this.#drawPaddles();

    requestAnimationFrame(this.#update.bind(this));
  }

  #constrainPaddles() {
    if (this.#leftPaddle.y < 0) this.#leftPaddle.y = 0;
    else if (this.#leftPaddle.y + this.#paddleHeight > this.#canvas.height)
      this.#leftPaddle.y = this.#canvas.height - this.#paddleHeight;

    if (this.#rightPaddle.y < 0) this.#rightPaddle.y = 0;
    else if (this.#rightPaddle.y + this.#paddleHeight > this.#canvas.height)
      this.#rightPaddle.y = this.#canvas.height - this.#paddleHeight;
  }

  #updateBallPosition() {
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
    this.#checkPaddleCollision();
  }

  #checkPaddleCollision() {
    if (
      this.#ball.x - this.#ball.radius <=
        this.#leftPaddle.x + this.#paddleWidth &&
      this.#ball.y > this.#leftPaddle.y &&
      this.#ball.y < this.#leftPaddle.y + this.#paddleHeight
    ) {
      this.#ball.speedX = -this.#ball.speedX;
      this.#ball.speedY += (Math.random() - 0.5) * 2;
    }

    if (
      this.#ball.x + this.#ball.radius >= this.#rightPaddle.x &&
      this.#ball.y > this.#rightPaddle.y &&
      this.#ball.y < this.#rightPaddle.y + this.#paddleHeight
    ) {
      this.#ball.speedX = -this.#ball.speedX;
      this.#ball.speedY += (Math.random() - 0.5) * 2;
    }
  }

  #checkScoring() {
    if (this.#ball.x - this.#ball.radius <= 0) {
      this.#player2.score++;
      this.#updateScores();
      this.#resetBall();
      this.#checkWin(this.#player2.name);
    }

    if (this.#ball.x + this.#ball.radius >= this.#canvas.width) {
      this.#player1.score++;
      this.#updateScores();
      this.#resetBall();
      this.#checkWin(this.#player1.name);
    }
  }

  #resetBall() {
    this.#ball.x = this.#canvas.width / 2;
    this.#ball.y = this.#canvas.height / 2;
    this.#ball.speedX = this.#ballSpeed * (Math.random() < 0.5 ? 1 : -1);
    this.#ball.speedY = this.#ballSpeed * (Math.random() < 0.5 ? 1 : -1);
  }

  #checkWin(winner) {
    if (
      this.#player1.score >= this.#winScore ||
      this.#player2.score >= this.#winScore
    ) {
      this.#isGameStarted = false;
      if (this.#onMatchEnd) {
        this.#onMatchEnd(winner);
      }
    }
  }

  #drawField() {
    this.#ctx.setLineDash([5, 5]);
    this.#ctx.beginPath();
    this.#ctx.moveTo(this.#canvas.width / 2, 0);
    this.#ctx.lineTo(this.#canvas.width / 2, this.#canvas.height);
    this.#ctx.strokeStyle = "white";
    this.#ctx.stroke();
  }

  #drawPaddles() {
    this.#ctx.fillStyle = "#60A5FA";
    this.#ctx.fillRect(
      this.#leftPaddle.x,
      this.#leftPaddle.y,
      this.#paddleWidth,
      this.#paddleHeight
    );
    this.#ctx.fillRect(
      this.#rightPaddle.x,
      this.#rightPaddle.y,
      this.#paddleWidth,
      this.#paddleHeight
    );
  }

  #drawBall() {
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

  #userSettings() {
    document.querySelector("#player1username").innerText = this.#player1.name;
    document.querySelector("#player2username").innerText = this.#player2.name;
  }

  #updateScores() {
    document.querySelector("#player1score").textContent = this.#player1.score;
    document.querySelector("#player2score").textContent = this.#player2.score;
    if (this.#player1.score >= this.#winScore) {
      this.#isGameStarted = false;
    } else if (this.#player2.score >= this.#winScore) {
      this.#isGameStarted = false;
    }
  }
}
