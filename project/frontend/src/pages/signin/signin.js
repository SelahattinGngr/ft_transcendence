import { Toast } from "../../components/toast.js";

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
    localStorage.setItem("access_token", data.data.access_token.token);
    localStorage.setItem("refresh_token", data.data.refresh_token.token);
    localStorage.setItem("username", data.data.username);
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
    console.error("Error during sign in:", error);
  }
}
