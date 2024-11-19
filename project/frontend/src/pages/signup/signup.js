import { Toast } from "../../components/toast.js";

export async function handleSignup(event) {
  event.preventDefault();
  const username = document.getElementById("signupUsername").value;
  const email = document.getElementById("signupEmail").value;
  const password = document.getElementById("signupPassword").value;
  const first_name = document.getElementById("signupFirstName").value;
  const last_name = document.getElementById("signupLastName").value;
  const avatar_url = document.getElementById("signupAvatarUrl").value;

  try {
    const response = await fetch("http://localhost:8000/auth/signup/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Accept-Language": "tr",
      },
      body: JSON.stringify({
        username,
        email,
        password,
        first_name,
        last_name,
        avatar_url,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      return Toast({
        title: "Error",
        message: data.error,
        theme: "danger",
      });
    }
    Toast({
      title: "Success",
      message: data.data.success,
      theme: "success",
    });
    window.location.hash = "signin";
  } catch (error) {
    console.error("Error during sign up:", error);
  }
}
