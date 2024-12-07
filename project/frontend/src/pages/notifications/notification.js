import { Toast } from "../../components/toast.js";

export async function getNotifications() {
  try {
    const response = await fetch(
      "http://localhost:8000/notification/get-notifications/",
      {
        method: "GET",
        headers: {
          "Accept-Language": "tr",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      }
    );

    const data = (await response.json()).data;

    if (!response.ok) {
      throw new Error(data.error);
    }
    const notificationList = document.querySelector("#notificationList");
    data.forEach((notification) => {
      const listItem = document.createElement("li");
      listItem.classList.add("list-group-item");

      const title = document.createElement("strong");
      title.id = "type";
      title.textContent = notification.type;

      const content = document.createElement("span");
      content.id = "content";
      content.textContent = ` ${notification.content} - ${notification.sender_username}`;

      listItem.appendChild(title);
      listItem.appendChild(content);
      notificationList.appendChild(listItem);
    });
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error getting notifications:", error);
  }
}
