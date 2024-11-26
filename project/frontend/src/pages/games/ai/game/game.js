export function aiGame(
  user,
  ballSpeed,
  gameDifficulty,
  paddleHeight,
  winScore
) {
  window.location.hash = "games/ai/game";
  console.log("user: ", user);
  console.log("gameDifficulty: ", gameDifficulty); // oyun zorluguna gore ai paddle hizi degisecek
  console.log("ballSpeed: ", ballSpeed);
  console.log("paddleHeight: ", paddleHeight);
  console.log("winScore: ", winScore);
}
