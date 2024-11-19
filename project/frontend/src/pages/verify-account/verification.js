import { Toast } from "../../components/toast.js";

export async function verificationCode() {
  const verificationToken = window.location.hash.split("?")[1];
  if (!verificationToken) {
    return Toast({
      title: "Error",
      message: "Invalid verification token",
    });
  }
  try {
    const response = await fetch(
      `http://localhost:8000/auth/verify-account/${verificationToken}`
    );
    const data = await response.json();
    await new Promise((resolve) => setTimeout(resolve, 2000));
    if (response.ok) {
      Toast({
        title: "Success",
        message: data.data.success,
        theme: "success",
      });
      window.location.hash = "home";
      return;
    }
    Toast({
      title: "Error",
      theme: "danger",
      message: data.error,
    });
    // TODO: retry verify account page yapılacak ve oraya yönlendirilecek
    window.location.hash = "home";
  } catch (error) {
    console.error("Error during verification:", error);
  }
}
