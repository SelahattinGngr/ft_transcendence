import { Toast } from "../../../components/toast.js";
import { getLanguage } from "../../../utils/language.js";

export async function fetchUserProfile(userName) {
  try {
    const response = await fetch(
      `https://k2m10s01.42kocaeli.com.tr:8080/api/user/${userName}`,
      {
        method: "GET",
        headers: {
          "Accept-Language": getLanguage(),
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      }
    );

    const { data, error } = await response.json();
    if (!response.ok) {
      throw new Error(error);
    }

    document.querySelector("#profile-avatar").src = data.avatar_url;
    document.querySelector("#profile-username").textContent = data.username;
    document.querySelector("#profile-bio").textContent =
      data.bio || "Bio not provided";
    document.querySelector("#profile-firstname").textContent = data.first_name;
    document.querySelector("#profile-lastname").textContent = data.last_name;
    document.querySelector("#profile-email").textContent = data.email;
    loadMatchHistory(userName);
  } catch (error) {
    Toast({
      type: "error",
      message: error.message,
      theme: "danger",
    });
  }
}

async function loadMatchHistory(username) {
  try {
    const response = await fetch(
      `https://k2m10s01.42kocaeli.com.tr:8080/api/game/get-history/${username}`,
      {
        method: "GET",
        headers: {
          "Accept-Language": getLanguage(),
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      }
    );

    const { data, error } = await response.json();
    const matchHistoryContainer = document.querySelector("#match-history");
    if (!response.ok) {
      matchHistoryContainer.innerHTML =
        "<p>Ahmet gardaşım tam burada maç sonucu için off'a bass</p>";
      throw new Error(error);
    }

    if (data.length === 0) {
      matchHistoryContainer.innerHTML = "<p>No match history</p>";
      return;
    }

    const matchHistory = data.map((match) => {
      return `
        <div class="card mb-3 text-bg-${match.isWin ? "success" : "danger"}">
          <div class="card-body">
            <h5 class="card-title">${match.username} vs ${match.aiName}</h5>
            <p class="card-text">${match.userScore} - ${match.aiScore}</p>
            <p class="card-text">${match.created_at}</p>
          </div>
        </div>
      `;
    });

    matchHistoryContainer.innerHTML = matchHistory.join("");
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
  }
}
