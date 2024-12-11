import { Toast } from "../../components/toast.js";
import { getLanguage } from "../../utils/language.js";

export async function loadProfile() {
  const username = localStorage.getItem("username");
  if (!username) {
    console.error("No username found in localStorage");
    return;
  }

  try {
    const response = await fetch(
      `http://localhost:8000/api/user/${username}/`,
      {
        method: "GET",
        headers: {
          "Accept-Language": "tr",
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

    setupBioUpdate(data.bio);
    loadMatchHistory();
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
  }
}

function setupBioUpdate(currentBio) {
  const updateBioBtn = document.querySelector("#update-bio-btn");
  const bioInput = document.querySelector("#bio-input");
  const saveBioBtn = document.querySelector("#save-bio-btn");
  const username = localStorage.getItem("username");
  if (!username) {
    console.error("No username found in localStorage");
    return;
  }

  updateBioBtn.addEventListener("click", () => {
    bioInput.value = currentBio || "";
    new bootstrap.Modal(document.querySelector("#bioModal")).show();
  });

  saveBioBtn.addEventListener("click", async () => {
    const bio = bioInput.value.trim();
    try {
      console.log("Sending bio update request...");
      const response = await fetch(
        `http://localhost:8000/api/user/update/${username}/`,
        {
          method: "PUT",
          headers: {
            "Accept-Language": getLanguage(),
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({ bio }),
        }
      );

      const { data, error } = await response.json();
      if (!response.ok) {
        throw new Error(error);
      }

      document.querySelector("#profile-bio").textContent = bio;
      bootstrap.Modal.getInstance(document.querySelector("#bioModal")).hide();
      Toast({
        title: "Success",
        message: "Bio updated successfully",
        theme: "success",
      });
    } catch (error) {
      Toast({
        title: "Error",
        message: error.message,
        theme: "danger",
      });
    }
  });
}

async function loadMatchHistory() {
  try {
    const username = localStorage.getItem("username");
    const response = await fetch(
      `http://localhost:8000/api/game/get-history/${username}`,
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