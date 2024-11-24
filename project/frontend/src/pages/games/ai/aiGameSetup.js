import { aiGame } from "./game/game.js";

export async function aiGameSetup(event) {
  event.preventDefault();
  const user = document.getElementById("gamerusername").value;
  const ballSpeed = document.getElementById("ballSpeed").value;
  const gameDifficulty = document.getElementById("gameDifficulty").value;
  const paddleHeight = document.getElementById("paddleHeight").value;
  const winScore = document.getElementById("winScore").value;

  aiGame(user, ballSpeed, gameDifficulty, paddleHeight, winScore);
}
