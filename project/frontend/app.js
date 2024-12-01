import { Toast } from "./src/components/toast.js";
import { aiGameSetup } from "./src/pages/games/ai/aiGameSetup.js";
import { localeTournamentSetup } from "./src/pages/games/locale-tournament/localeTournamentGameSetup.js";
import { canvasSetup } from "./src/pages/games/locale/game/game.js";
import { localeGameSetup } from "./src/pages/games/locale/localeGameSetup.js";
import { homeActions } from "./src/pages/home/home.js";
import { loadProfile } from "./src/pages/profile/profile.js";
import { retryVerifyAccount } from "./src/pages/retry-verify-account/retry.js";
import { handleSignin, intraSignin } from "./src/pages/signin/signin.js";
import { handleSignup } from "./src/pages/signup/signup.js";
import { verificationCode } from "./src/pages/verify-account/verification.js";
import { active } from "./src/utils/active.js";
import { isAuth } from "./src/utils/isAuth.js";
import {
  setuplanguage,
  loadlanguage,
  changelanguage,
  getLanguage,
} from "./src/utils/language.js";

window.changelanguage = changelanguage;
window.signout = signout;

document.addEventListener("DOMContentLoaded", async function () {
  const hash = window.location?.hash?.slice(1) ?? "home";
  const page = hash.split("?")[0];
  await loadPage(page);
  active(page);
  loadlanguage();
});

window.addEventListener("hashchange", async function () {
  const hash = window.location?.hash?.slice(1) ?? "home";
  const page = hash.split("?")[0];
  await loadPage(page);
  active(page);
});

async function loadPage(page) {
  try {
    // TODO: window.location.pathname kullanarak sayfa yolunu değiştirebilirsiniz.
    if (page === "") {
      page = "home";
      window.location.hash = "#home";
    }
    const filePath = `/src/pages/${page}/`;
    const response = await fetch(filePath);
    if (!response.ok) {
      throw new Error("Page not found");
    }
    const html = await response.text();
    document.getElementById("app").innerHTML = html;
    setupPageActions(page);
    await setuplanguage();
  } catch (error) {
    loadPage("not-found");
    console.error("Error loading page:", page);
    console.error("Error loading error:", error);
  }
}

function setupPageActions(page) {
  authButtons();
  if (page === "") {
    // window.location.pathname kullanarak sayfa yolunu değiştirebilirsiniz.
    window.location.hash = "home";
  }
  if (page === "home") {
    homeActions();
  } else if (page === "signin") {
    submitHandler("signinForm", handleSignin);
    document
      .querySelector("#ecole-button-submit")
      .addEventListener("click", intraSignin);
  } else if (page === "signup") {
    submitHandler("signupForm", handleSignup);
  } else if (page === "profile") {
    loadProfile();
  } else if (page === "verify-account") {
    verificationCode();
  } else if (page === "not-found") {
    const randomNumber = Math.floor(Math.random() * 33) + 1;
    document.getElementById(
      "not-found-image"
    ).src = `/src/assets/errors/${randomNumber}.svg`;
  } else if (page === "retry-verify-account") {
    submitHandler("retryForm", retryVerifyAccount);
  } else if (page === "games/locale") {
    putRange("#ballSpeed", "#rangeValue");
    submitHandler("localeGamesForm", localeGameSetup);
  } else if (page === "games/locale-tournament") {
    putRange("#ballSpeed", "#rangeValue");
    submitHandler("localeTournamentGamesForm", localeTournamentSetup);
  } else if (page === "games/ai") {
    putRange("#ballSpeed", "#rangeValue");
    putRange("#gameDifficulty", "#difficultyRangeValue");
    submitHandler("aiGamesForm", aiGameSetup);
  } else if (page === "games/locale/game") {
    canvasSetup();
  }
}

function submitHandler(elementId, eventListener) {
  document.getElementById(elementId).addEventListener("submit", eventListener);
}

function putRange(querySelector, id) {
  document.querySelector(querySelector).addEventListener("input", (e) => {
    document.querySelector(id).innerHTML = e.target.value;
  });
}

async function signout() {
  const accessToken = localStorage.getItem("access_token");
  if (!accessToken) {
    alert("No active session found.");
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/auth/signout/", {
      method: "GET",
      headers: {
        "Accept-Language": getLanguage(),
        Authorization: `Bearer ${accessToken}`,
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error);
    }
    Toast({
      title: "Success",
      message: data.data.success,
      theme: "success",
    });
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("username");
    authButtons();
  } catch (error) {
    console.error("Error during logout:", error);
    Toast({
      title: "Error",
      message: data.error,
      theme: "danger",
    });
  }
}

function authButtons() {
  const authContainer = document.querySelector("#auth");
  const profileDropdown = document.querySelector("#profile-dropdown");

  if (isAuth()) {
    authContainer.classList.remove("d-flex");
    authContainer.classList.add("d-none");

    profileDropdown.classList.remove("d-none");
    profileDropdown.classList.add("d-flex");
  } else {
    profileDropdown.classList.remove("d-flex");
    profileDropdown.classList.add("d-none");

    authContainer.classList.remove("d-none");
    authContainer.classList.add("d-flex");
  }
}
