import { Toast } from "../../../components/toast.js";
import { getLanguage } from "../../../utils/language.js";

export async function fetchUserProfile(userName) {
  console.log(userName);
  try {
    const response = await fetch(`http://localhost:8000/api/user/${userName}`, {
      method: "GET",
      headers: {
        "Accept-Language": getLanguage(),
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });

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
    loadMatchHistory();
  } catch (error) {
    Toast({
      type: "error",
      message: error.message,
      theme: "danger",
    });
  }
}

function loadMatchHistory() {
  const matchHistoryContainer = document.getElementById("match-history");
  matchHistoryContainer.innerHTML =
    "<p>Ahmet gardaşım tam burada maç sonucu için off'a bass</p>";
}
