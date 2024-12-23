import {
  getTemporaryData,
  removeTemporaryData,
} from "../../../../utils/temporaryLocaleStorage.js";
import { Toast } from "../../../../components/toast.js";

export class Game {
  #canvas = document.getElementById("gameCanvas");
  #ctx = this.#canvas.getContext("2d");
  #data = getTemporaryData("localeGameData");
  constructor() {
    if (!this.#data) {
      window.location.hash = "games/locale";
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

  #player1 = { name: "Player 1", score: 0 };
  #player2 = { name: "Player 2", score: 0 };
  #ballSpeed = parseInt(this.#data.ballSpeed, 10);
  #ballSize = 7.5;
  #paddleHeight = parseInt(this.#data.paddleHeight, 10) / 2;
  #paddleWidth = 10;
  #paddleSpeed = parseInt(this.#data.ballSpeed, 10) * 1.75;
  #winScore = parseInt(this.#data.winScore, 10);

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

    document.addEventListener("keydown", (event) => {
      if (event.key === "w") this.#leftPaddle.dy = -this.#paddleSpeed;
      if (event.key === "s") this.#leftPaddle.dy = this.#paddleSpeed;
      if (event.key === "ArrowUp") this.#rightPaddle.dy = -this.#paddleSpeed;
      if (event.key === "ArrowDown") this.#rightPaddle.dy = this.#paddleSpeed;
    });

    document.addEventListener("keyup", (event) => {
      if (event.key === "w" || event.key === "s") this.#leftPaddle.dy = 0;
      if (event.key === "ArrowUp" || event.key === "ArrowDown")
        this.#rightPaddle.dy = 0;
    });
    this.#userSettings();
    this.#update();
  }

  #update() {
    if (!this.#isGameStarted) return;

    // Update paddle positions
    this.#leftPaddle.y += this.#leftPaddle.dy;
    this.#rightPaddle.y += this.#rightPaddle.dy;

    // Constrain paddles within the canvas
    if (this.#leftPaddle.y < 0) this.#leftPaddle.y = 0;
    else if (this.#leftPaddle.y + this.#paddleHeight > this.#canvas.height)
      this.#leftPaddle.y = this.#canvas.height - this.#paddleHeight;

    if (this.#rightPaddle.y < 0) this.#rightPaddle.y = 0;
    else if (this.#rightPaddle.y + this.#paddleHeight > this.#canvas.height)
      this.#rightPaddle.y = this.#canvas.height - this.#paddleHeight;

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
        this.#leftPaddle.x + this.#paddleWidth &&
      this.#ball.y > this.#leftPaddle.y &&
      this.#ball.y < this.#leftPaddle.y + this.#paddleHeight
    ) {
      this.#ball.speedX = -this.#ball.speedX;
      // Randomize the vertical speed after collision
      this.#ball.speedY += (Math.random() - 0.5) * 2;
    }

    if (
      this.#ball.x + this.#ball.radius >= this.#rightPaddle.x &&
      this.#ball.y > this.#rightPaddle.y &&
      this.#ball.y < this.#rightPaddle.y + this.#paddleHeight
    ) {
      this.#ball.speedX = -this.#ball.speedX;
      // Randomize the vertical speed after collision
      this.#ball.speedY += (Math.random() - 0.5) * 2;
    }

    // Scoring system
    if (this.#ball.x - this.#ball.radius <= 0) {
      this.#player2.score++;
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
    this.#drawDashedField();
    this.#drawBall();
    this.#drawPaddles();

    requestAnimationFrame(this.#update.bind(this));
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

  #drawDashedField() {
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
    this.#ball.speedX = this.#ballSpeed * (Math.random() < 0.5 ? 1 : -1);
    this.#ball.speedY = this.#ballSpeed * (Math.random() < 0.5 ? 1 : -1);
    this.#ball.speedY += (Math.random() - 0.5) * 0.5;
  }

  #userSettings() {
    document.querySelector("#player1username").innerText = this.#player1.name;
    document.querySelector("#player2username").innerText = this.#player2.name;
  }

  #updateScores() {
    document.querySelector("#player1score").innerText = this.#player1.score;
    document.querySelector("#player2score").innerText = this.#player2.score;
    if (this.#player1.score >= this.#winScore) {
      this.#isGameStarted = false;
      this.#gameOver(this.#player1.name);
    } else if (this.#player2.score >= this.#winScore) {
      this.#isGameStarted = false;
      this.#gameOver(this.#player2.name);
    }
  }

  #gameOver(winner) {
    this.#isGameStarted = false;
    removeTemporaryData("localeGameData");
    Toast({
      title: "Game Over",
      message: `${winner} wins!`,
      theme: "success",
    });
    setTimeout(() => {
      window.location.hash = "games/locale";
    }, 3000);
  }
}
