// import { getTemporaryData } from "../../../../utils/temporaryLocaleStorage.js";

// const Canvas = {
//   canvas: {
//     width: 1000,
//     height: 500,
//   },
// };

// const Player1 = {
//   name: "Player 1",
//   score: 0,
// };

// const Player2 = {
//   name: "Player 2",
//   score: 0,
// };

// /* Game settings */
// function setLocalGame(newLocalGame) {
//   LocalGame = { ...LocalGame, ...newLocalGame };
// }

// const LocalGame = {
//   winScore: 5,

//   ballSpeed: 5,
//   ballSize: 10,

//   paddleWidth: 10,
//   paddleHeight: 100,
// };
// /* Game settings */

// const rightPaddle = {
//   x: Canvas.canvas.width - paddleWidth - 20,
//   y: Canvas.canvas.height / 2 - paddleHeight / 2,
//   dy: 0,
// };

// const leftPaddle = {
//   x: 20,
//   y: Canvas.canvas.height / 2 - paddleHeight / 2,
//   dy: 0,
// };

// const ball = {
//   x: Canvas.canvas.width / 2,
//   y: Canvas.canvas.height / 2,
//   radius: ballSize,
//   speedX: 5,
//   speedY: 5,
// };

export function canvasSetup() {
  //   try {
  //     const data = getTemporaryData("localeGameData");
  //     if (!data) {
  //       window.location.hash = "games/locale";
  //       return;
  //     }
  //     const {
  //       users: [player1name, player2name],
  //       ballSpeed,
  //       paddleHeight,
  //       winScore,
  //     } = data;
  //     Canvas.canvas = document.querySelector("#gameCanvas");
  //     const ctx = Canvas.canvas.getContext("2d");
  //     setLocalGame({ ballSpeed, paddleHeight, winScore });
  //     Player1.name = player1name;
  //     Player2.name = player2name;
  //     userSettings();
  //   } catch (error) {
  //     if (window.location.hash === "#games/locale/game") {
  //       console.error(error);
  //     }
  //   }
}

// function userSettings() {
//   document.querySelector("#player1username").textContent = Player1.name;
//   document.querySelector("#player2username").textContent = Player2.name;
// }

// function updateScores() {
//   document.querySelector("#player1score").textContent = Player1.score;
//   document.querySelector("#player2score").textContent = Player2.score;
// }
