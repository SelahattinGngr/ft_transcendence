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
      `https://k2m10s01.42kocaeli.com.tr:8080/api/auth/verify-account/${verificationToken}`
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
    window.location.hash = "retry-verify-account";
  } catch (error) {
    console.error("Error during verification:", error);
  }
}
