import { authButtons } from "../../utils/authButtons.js";
import { getLanguage } from "../../utils/language.js";
import { Toast } from "../../components/toast.js";

export async function otp(event) {
  event.preventDefault();
  window.location.hash = "home";

  const otp1 = document.getElementById("otp1").value;
  const otp2 = document.getElementById("otp2").value;
  const otp3 = document.getElementById("otp3").value;
  const otp4 = document.getElementById("otp4").value;
  const code = otp1 + otp2 + otp3 + otp4;

  try {
    const username = localStorage.getItem("username");
    if (!username) {
      window.location.hash = "signin";
    }
    const response = await fetch("http://localhost:8000/auth/two-factor/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept-Language": getLanguage(),
      },
      body: JSON.stringify({ username, code }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error);
    }
    localStorage.setItem("access_token", data.data.access_token.token);
    localStorage.setItem("refresh_token", data.data.refresh_token.token);
    authButtons();
    Toast({
      title: "Success",
      message: "You have successfully signed in.",
      theme: "success",
    });
    window.location.hash = "home";
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error during otp:", error);
    window.location.hash = "signin";
  }
}

export function moveToNext(current, nextFieldID) {
  if (current.value.length >= current.maxLength) {
    if (nextFieldID) {
      document.getElementById(nextFieldID).focus();
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    const otp1 = document.getElementById("otp1");
    if (otp1) {
      otp1.focus();//
    }
  }, 10);
});
