import { setTemporaryData } from "../../../utils/temporaryLocaleStorage.js";

export async function aiGameSetup(event) {
  event.preventDefault();
  const user = document.getElementById("gamerusername").value;
  const ballSpeed = document.getElementById("ballSpeed").value;
  const gameDifficulty = document.getElementById("gameDifficulty").value;
  const paddleHeight = document.getElementById("paddleHeight").value;
  const winScore = document.getElementById("winScore").value;

  setTemporaryData(
    "aiGameData",
    { users: [user], ballSpeed, gameDifficulty, paddleHeight, winScore },
    2
  );
  window.location.hash = "games/ai/game";
}
