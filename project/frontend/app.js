import { homeActions } from "./src/pages/home/home.js";
import { loadProfile } from "./src/pages/profile/profile.js";
import { retryVerifyAccount } from "./src/pages/retry-verify-account/retry.js";
import { handleSignin } from "./src/pages/signin/signin.js";
import { handleSignup } from "./src/pages/signup/signup.js";
import { verificationCode } from "./src/pages/verify-account/verification.js";
import { active } from "./src/utils/Active.js";
import { isAuth } from "./src/utils/isAuth.js";
import {
  setuplanguage,
  loadlanguage,
  changelanguage,
} from "./src/utils/language.js";

window.changelanguage = changelanguage;

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
  if (page === "home") {
    homeActions();
  } else if (page === "signin") {
    document
      .getElementById("signinForm")
      .addEventListener("submit", handleSignin);
  } else if (page === "signup") {
    document
      .getElementById("signupForm")
      .addEventListener("submit", handleSignup);
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
    document
      .getElementById("retryForm")
      .addEventListener("submit", retryVerifyAccount);
  }
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
        "Accept-Language": "tr",
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response.ok) {
      alert("Logout successful!");
      localStorage.clear(); // Tüm localStorage'ı temizle
    } else {
      const errorData = await response.json();
      console.error("Logout failed:", errorData.message);
      alert("Logout failed: " + (errorData.message || "Unknown error"));
    }
  } catch (error) {
    console.error("Error during logout:", error);
    alert("Error during logout. Please try again.");
  }
}

function authButtons() {
  if (isAuth()) {
    document.querySelector("#auth").classList.add("d-none");
    document.querySelector("#profile-dropdown").classList.add("d-flex");
    return;
  }
  document.querySelector("#profile-dropdown").classList.add("d-none");
  document.querySelector("#auth").classList.add("d-flex");
}
