import { Toast } from "../../components/toast.js";

export async function retryVerifyAccount(event) {
  event.preventDefault();
  const email = document.getElementById("retry-verify-email").value;
  console.log(email);
  try {
    const response = await fetch(
      "https://k2m10s01.42kocaeli.com.tr:8080/api/auth/retry-verify-account/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept-Language": "tr",
        },
        body: JSON.stringify({ email }),
      }
    );

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
    window.location.hash = "home";
  } catch (error) {
    Toast({
      title: "Error",
      message: "Iternal server error",
      theme: "danger",
    });
    console.error("Error during retry verification email:", error);
  }
}
