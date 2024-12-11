import { Toast } from "../components/toast.js";
import { authButtons } from "./authButtons.js";
import { getLanguage } from "./language.js";

export async function signout() {
  const accessToken = localStorage.getItem("access_token");
  if (!accessToken) {
    alert("No active session found.");
    return;
  }

  try {
    const response = await fetch(
      "https://k2m10s01.42kocaeli.com.tr:8080/api/auth/signout/",
      {
        method: "GET",
        headers: {
          "Accept-Language": getLanguage(),
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

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
    window.location.hash = "home";
  } catch (error) {
    console.error("Error during logout:", error);
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
  }
}
