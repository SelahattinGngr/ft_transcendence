import { Toast } from "../../components/toast.js";

export async function getNotifications() {
  try {
    const response = await fetch(
      "http://localhost:8000/notification/get-notifications",
      {
        method: "GET",
        headers: {
          "Accept-Language": "tr",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error);
    }
    console.log(data.data);
    document.getElementById("content").textContent = data.data;
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error getting notifications:", error);
  }
}
