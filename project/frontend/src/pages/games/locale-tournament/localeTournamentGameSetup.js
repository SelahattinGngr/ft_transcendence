import { aiGame } from "./game/game.js";

export async function localeTournamentSetup(event) {
  event.preventDefault();
  const user1 = document.getElementById("gamer1username").value;
  const user2 = document.getElementById("gamer2username").value;
  const user3 = document.getElementById("gamer3username").value;
  const user4 = document.getElementById("gamer4username").value;
  const users = { user1, user2, user3, user4 };
  const ballSpeed = document.getElementById("ballSpeed").value;
  const paddleHeight = document.getElementById("paddleHeight").value;
  const winScore = document.getElementById("winScore").value;

  aiGame(users, ballSpeed, paddleHeight, winScore);
}
