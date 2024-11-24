import { setTemporaryData } from "../../../utils/temporaryLocaleStorage.js";

export async function localeGameSetup(event) {
  event.preventDefault();
  const user1 = document.getElementById("gamer1username").value;
  const user2 = document.getElementById("gamer2username").value;
  const ballSpeed = document.getElementById("ballSpeed").value;
  const paddleHeight = document.getElementById("paddleHeight").value;
  const winScore = document.getElementById("winScore").value;

  setTemporaryData(
    "localeGameData",
    { users: [user1, user2], ballSpeed, paddleHeight, winScore },
    2
  );
  window.location.hash = "games/locale/game";
}
