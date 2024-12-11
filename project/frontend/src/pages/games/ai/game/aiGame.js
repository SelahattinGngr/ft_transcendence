import { Toast } from "../../../../components/toast.js";
import {
  getTemporaryData,
  removeTemporaryData,
} from "../../../../utils/temporaryLocaleStorage.js";

export class AiGame {
  #canvas = document.getElementById("gameCanvas");
  #ctx = this.#canvas.getContext("2d");
  #data = getTemporaryData("aiGameData");
  constructor() {
    if (!this.#data) {
      window.location.hash = "games/ai";
      return;
    }
    this.#player1 = {
      name: this.#data.users[0],
      score: 0,
    };
    this.#aiPlayer = {
      name: "MOULINETTE",
      score: 0,
    };
    this.#setAiDifficulty();
    this.#startGame();
  }

  #player1 = { name: "Player 1", score: 0 };
  #aiPlayer = { name: "MOULINETTE", score: 0 };
  #ballSpeed = parseInt(this.#data.ballSpeed, 10);
  #ballSize = 7.5;
  #paddleHeight = parseInt(this.#data.paddleHeight, 10) / 1.75;
  #paddleWidth = 10;
  #paddleSpeed = parseInt(this.#data.ballSpeed, 10) * 1.75;
  #winScore = parseInt(this.#data.winScore, 10);
  #aiSpeedMultiplier = parseInt(this.#data.gameDifficulty, 10);

  #isGameStarted = false;
  #ball = {
    x: this.#canvas.width / 2,
    y: this.#canvas.height / 2,
    radius: this.#ballSize,
    speedX: this.#ballSpeed,
    speedY: this.#ballSpeed,
  };
  #playerPaddle = {
    x: 0,
    y: this.#canvas.height / 2 - this.#paddleHeight / 2,
    dy: 0,
  };
  #aiPaddle = {
    x: this.#canvas.width - this.#paddleWidth,
    y: this.#canvas.height / 2 - this.#paddleHeight / 2,
    dy: this.#ball.speedY * this.#aiSpeedMultiplier,
  };

  #startGame() {
    if (this.#isGameStarted) return;
    this.#isGameStarted = true;

    document.addEventListener("keydown", (event) => {
      if (event.key === "w") this.#playerPaddle.dy = -this.#paddleSpeed;
      if (event.key === "s") this.#playerPaddle.dy = this.#paddleSpeed;
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
    else if (this.#playerPaddle.y + this.#paddleHeight > this.#canvas.height)
      this.#playerPaddle.y = this.#canvas.height - this.#paddleHeight;

    // Update AI paddle position based on difficulty level
    this.#aiPaddle.y += (this.#ball.y - this.#aiPaddle.y) * this.#aiPaddle.dy;

    if (this.#aiPaddle.y + parseInt(this.#data.gameDifficulty, 10) * 10 < 0)
      this.#aiPaddle.y = 0;
    else if (
      this.#aiPaddle.y +
        parseInt(this.#data.gameDifficulty, 10) * 10 +
        this.#paddleHeight >
      this.#canvas.height
    )
      this.#aiPaddle.y =
        this.#canvas.height -
        this.#paddleHeight -
        parseInt(this.#data.gameDifficulty, 10) * 10;

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
        this.#playerPaddle.x + this.#paddleWidth &&
      this.#ball.y > this.#playerPaddle.y &&
      this.#ball.y < this.#playerPaddle.y + this.#paddleHeight
    ) {
      this.#ball.speedX = -this.#ball.speedX;
      // Randomize the vertical speed after collision
      this.#ball.speedY += (Math.random() - 0.5) * 2.25;
    }

    if (
      this.#ball.x + this.#ball.radius >= this.#aiPaddle.x &&
      this.#ball.y >
        this.#aiPaddle.y - parseInt(this.#data.gameDifficulty, 10) * 5 &&
      this.#ball.y <
        this.#aiPaddle.y +
          this.#paddleHeight +
          parseInt(this.#data.gameDifficulty, 10) * 5
    ) {
      this.#ball.speedX = -this.#ball.speedX;
      // Randomize the vertical speed after collision
      this.#ball.speedY += (Math.random() - 0.5) * 2;
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
      this.#paddleWidth,
      this.#paddleHeight
    );
    this.#ctx.fillRect(
      this.#aiPaddle.x,
      this.#aiPaddle.y,
      this.#paddleWidth,
      this.#paddleHeight + parseInt(this.#data.gameDifficulty, 10) * 10
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
    this.#ball.speedX = this.#ballSpeed * (Math.random() < 0.5 ? 1 : -1);
    this.#ball.speedY = this.#ballSpeed * (Math.random() < 0.5 ? 1 : -1);
    this.#ball.speedY += (Math.random() - 0.5) * 0.5;
  }

  #userSettings() {
    document.querySelector("#player1username").innerText = this.#player1.name;
    document.querySelector("#aiusername").innerText = this.#aiPlayer.name;
  }

  #updateScores() {
    document.querySelector("#player1score").textContent = this.#player1.score;
    document.querySelector("#aiscore").textContent = this.#aiPlayer.score;
    if (this.#player1.score >= this.#winScore) {
      this.#isGameStarted = false;
      this.#gameOver(this.#player1.name);
    } else if (this.#aiPlayer.score >= this.#winScore) {
      this.#isGameStarted = false;
      this.#gameOver(this.#aiPlayer.name);
    }
  }

  #setAiDifficulty() {
    switch (this.#aiSpeedMultiplier) {
      case 1:
        this.#aiPaddle.dy = this.#ball.speedY * 0.02;
        break;
      case 2:
        this.#aiPaddle.dy = this.#ball.speedY * 0.04;
        break;
      case 3:
        this.#aiPaddle.dy = this.#ball.speedY * 0.06;
        break;
      case 4:
        this.#aiPaddle.dy = this.#ball.speedY * 0.08;
        break;
      default:
        this.#aiPaddle.dy = this.#ball.speedY * 0.12;
        break;
    }
  }

  #gameOver(winner) {
    this.#isGameStarted = false;
    removeTemporaryData("aiGameData");
    Toast({
      title: "Game Over",
      message: `${winner} wins!`,
      type: "success",
    });
    setTimeout(async () => {
      await this.#saveGame();
      window.location.hash = "games/ai";
    }, 3000);
  }

  async #saveGame() {
    try {
      const response = await fetch(
        "https://k2m10s01.42kocaeli.com.tr:8080/myapi/game/save-game/",
        {
          method: "POST",
          headers: {
            "Accept-Language": "tr",
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            username: this.#player1.name,
            userScore: this.#player1.score,
            aiScore: this.#aiPlayer.score,
            isWin: this.#player1.score > this.#aiPlayer.score,
          }),
        }
      );
      const { data, error } = await response.json();
      if (!response.ok) {
        throw new Error(error);
      }
    } catch (error) {
      Toast({
        title: "Error",
        message: error.message,
        type: "error",
      });
    }
  }
}
