import { Toast } from "../../components/toast.js";
import { getLanguage } from "../../utils/language.js";

export async function handleSignin(event) {
  event.preventDefault();
  const signin = document.getElementById("signinUsername").value;
  const password = document.getElementById("signinPassword").value;

  try {
    const response = await fetch("http://localhost:8000/auth/signin/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept-Language": "tr",
      },
      body: JSON.stringify({ signin, password }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error);
    }
    localStorage.setItem("username", data.data.username);
    Toast({
      title: "Success",
      message: data.data.message,
      theme: "success",
    });
    window.location.hash = "2fa";
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error during sign in:", error);
  }
}

export async function intraSignin() {
  try {
    const url = await getIntraUrl();
    const popup = createPopup(url);
    closePopupSettings(popup);
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error during intra:", error);
  }
}

async function getIntraUrl() {
  const response = await fetch("http://localhost:8000/auth/intra/", {
    method: "GET",
    headers: {
      "Accept-Language": "tr",
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error);
  }

  return data.data.url;
}

function createPopup(url) {
  const popupWidth = 600;
  const popupHeight = 600;
  const left = (window.innerWidth - popupWidth) / 2;
  const top = (window.innerHeight - popupHeight) / 2;

  return window.open(
    url,
    "OAuth2 Login",
    `width=${popupWidth},height=${popupHeight},top=${top},left=${left}`
  );
}

function closePopupSettings(popup) {
  const timer = setInterval(async function () {
    const urlParams = new URLSearchParams(popup.location.search);
    const code = urlParams.get("code");
    if (!!code) {
      console.log("Code:", code);
      clearInterval(timer);
      popup.close();
      const responseBackend = await fetch(
        `http://localhost:8000/auth/intra-callback/?code=${code}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept-Language": getLanguage(),
          },
          body: JSON.stringify({ code }),
        }
      );
      const data = await responseBackend.json();
      if (!responseBackend.ok) {
        throw new Error(data.error);
      }
      console.error("Data:", data);
      localStorage.setItem("access_token", data.data.access_token.token);
      localStorage.setItem("refresh_token", data.data.refresh_token.token);
      localStorage.setItem("username", data.data.username);
      Toast({
        title: "Success",
        message: "You have successfully signed in.",
        theme: "success",
      });
      window.location.hash = "home";
    }
  }, 1000);
}
