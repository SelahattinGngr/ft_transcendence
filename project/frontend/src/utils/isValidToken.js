import { Toast } from "../components/toast.js";
import { authButtons } from "./authButtons.js";
import { getLanguage } from "./language.js";

export async function isvalidToken() {
  const accessToken = localStorage.getItem("access_token");
  if (!accessToken) {
    return;
  }

  try {
    const response = await fetch(
      "https://k2m10s01.42kocaeli.com.tr:8080/api/auth/validate-token/",
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
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("username");
      authButtons();
      window.location.hash = "home";
      throw new Error(data.error);
    }
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error during token validation:", error);
  }
}
