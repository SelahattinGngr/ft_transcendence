import {
  getTemporaryData,
  setTemporaryData,
} from "../../../../utils/temporaryLocaleStorage.js";
import { Game } from "./game.js";

export class Tournament {
  #data = getTemporaryData("localeTournamentGameData");
  #players;
  #ballSpeed;
  #paddleHeight;
  #winScore;
  #matches = [];
  #currentMatchIndex = 0;
  #scores = {};

  constructor() {
    this.#players = Object.values(this.#data.users);
    this.#ballSpeed = parseInt(this.#data.ballSpeed, 10);
    this.#paddleHeight = parseInt(this.#data.paddleHeight, 10);
    this.#winScore = parseInt(this.#data.winScore, 10);

    if (this.#players.length % 2 !== 0) {
      throw new Error("Oyuncu sayısı çift olmalıdır!");
    }

    this.#initializeScores(this.#players);
    this.#generateMatches(this.#players);
    this.#startNextMatch(this.#ballSpeed, this.#paddleHeight, this.#winScore);
  }

  #initializeScores(players) {
    players.forEach((player) => {
      this.#scores[player] = 0;
    });
  }

  #generateMatches(players) {
    for (let i = 0; i < players.length; i += 2) {
      this.#matches.push([players[i], players[i + 1]]);
    }
  }

  #startNextMatch(ballSpeed, paddleHeight, winScore) {
    if (this.#currentMatchIndex >= this.#matches.length) {
      this.#endTournament();
      return;
    }

    const [player1, player2] = this.#matches[this.#currentMatchIndex];
    console.log(`Başlayan Maç: ${player1} vs ${player2}`);

    const data = {
      users: [player1, player2],
      ballSpeed,
      paddleHeight,
      winScore,
    };

    setTemporaryData("tournamentGameData", data, 2);

    const game = new Game();
    game.onMatchEnd((winner) => {
      this.#updateScores(winner);
      this.#currentMatchIndex++;
      this.#startNextMatch(ballSpeed, paddleHeight, winScore);
    });
  }

  #updateScores(winner) {
    this.#scores[winner]++;
  }

  #endTournament() {
    this.#startFinalMatches();
    const sortedScores = Object.entries(this.#scores).sort(
      (a, b) => b[1] - a[1]
    );
    console.log("Turnuva Sona Erdi!");
    console.log("Sonuçlar:");
    sortedScores.forEach(([player, score], index) => {
      console.log(`${index + 1}. ${player}: ${score} puan`);
    });
  }

  #startFinalMatches() {
    const winners = [];
    const losers = [];

    // Determine winners and losers from the initial matches
    this.#matches.forEach(([player1, player2], index) => {
      const winner =
        this.#scores[player1] > this.#scores[player2] ? player1 : player2;
      const loser =
        this.#scores[player1] > this.#scores[player2] ? player2 : player1;
      winners.push(winner);
      losers.push(loser);
    });

    // Winners match
    const [winner1, winner2] = winners;
    console.log(`Kazananlar Maçı: ${winner1} vs ${winner2}`);
    const winnersMatchData = {
      users: [winner1, winner2],
      ballSpeed: this.#ballSpeed,
      paddleHeight: this.#paddleHeight,
      winScore: this.#winScore,
    };
    setTemporaryData("tournamentGameData", winnersMatchData, 2);

    const winnersGame = new Game();
    winnersGame.onMatchEnd((winner) => {
      console.log(`1. ${winner}`);
      const runnerUp = winner === winner1 ? winner2 : winner1;
      console.log(`2. ${runnerUp}`);
      this.#scores[winner] = 3;
      this.#scores[runnerUp] = 2;
      this.#startLosersMatch(losers);
    });
  }

  #startLosersMatch(users) {
    const [loser1, loser2] = users;
    const losersMatchData = {
      users,
      ballSpeed: this.#ballSpeed,
      paddleHeight: this.#paddleHeight,
      winScore: this.#winScore,
    };
    setTemporaryData("tournamentGameData", losersMatchData, 2);

    const losersGame = new Game();
    losersGame.onMatchEnd((winner) => {
      console.log(`3. ${winner}`);
      const fourthPlace = winner === loser1 ? loser2 : loser1;
      console.log(`4. ${fourthPlace}`);
      this.#scores[winner] = 1;
      this.#scores[fourthPlace] = 0;
      this.#printCanvasScores();
    });
    console.log(`Kaybedenler Maçı: ${loser1} vs ${loser2}`);
  }

  #printCanvasScores() {
    const oldCanvas = document.getElementById("gameCanvas");
    if (oldCanvas) {
      oldCanvas.remove();
    }
    document.querySelector("#scoreBoard").remove();
    const newCanvas = document.createElement("canvas");
    newCanvas.id = "gameCanvas";
    newCanvas.width = 1000;
    newCanvas.height = 500;
    document.querySelector("#layout").appendChild(newCanvas);

    const ctx = newCanvas.getContext("2d");
    ctx.font = "20px Arial";
    ctx.fillStyle = "white";
    const sortedScores = Object.entries(this.#scores).sort(
      (a, b) => b[1] - a[1]
    );

    sortedScores.forEach(([player, score], index) => {
      ctx.fillText(
        `${index + 1}. ${player}: ${score} puan`,
        newCanvas.width / 2 - 100,
        30 + index * 30
      );
    });
    localStorage.removeItem("tournamentGameData");
    localStorage.removeItem("localeTournamentGameData");

    setTimeout(() => {
      window.location.hash = "games/locale-tournament";
    }, 5000);
  }
}
