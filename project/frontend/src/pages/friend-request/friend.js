import { Toast } from "../../components/toast.js";
import { getLanguage } from "../../utils/language.js";

export async function sendFriendRequest(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const friendUsername = formData.get("friendUsername");
  try {
    if (!friendUsername) {
      throw new Error("Please enter a username");
    }
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
      throw new Error("No active session found.");
    }
    const response = await fetch("http://localhost:8000/friend/send-request/", {
      method: "POST",
      headers: {
        "Accept-Language": getLanguage(),
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ friend_username: friendUsername }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error);
    }
    Toast({
      title: "Success",
      message: data.data.message,
      theme: "success",
    });
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
  }
}
