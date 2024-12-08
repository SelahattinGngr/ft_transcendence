import { Toast } from "../../components/toast.js";
import { setuplanguage } from "../../utils/language.js";

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
    notificationList.innerHTML = "";
    data.forEach((notification) => {
      const listItem = document.createElement("li");
      listItem.classList.add("list-group-item");

      const title = document.createElement("strong");
      title.id = "type";
      title.textContent = notification.type + ": ";

      title.setAttribute(
        "data-lang-path",
        "notification.title." + notification.type
      );

      const content = document.createElement("span");
      content.id = "content";
      content.textContent = " " + notification.content;
      content.setAttribute(
        "data-lang-path",
        "notification.content." + notification.type
      );

      const href = document.createElement("a");
      href.href = "#profile/" + notification.sender_username;
      href.textContent = notification.sender_username;

      const readButton = document.createElement("button");
      readButton.classList.add("btn", "btn-primary");
      readButton.textContent = "Read";
      readButton.addEventListener("click", (e) =>
        readNotification(e, notification.id)
      );

      const requestAcceptButton = document.createElement("button");
      requestAcceptButton.classList.add("btn", "btn-success");
      requestAcceptButton.textContent = "Accept";
      requestAcceptButton.addEventListener("click", (e) =>
        acceptRequest(e, notification.id)
      );

      const requestRejectButton = document.createElement("button");
      requestRejectButton.classList.add("btn", "btn-danger");
      requestRejectButton.textContent = "Reject";
      requestRejectButton.addEventListener("click", (e) =>
        rejectRequest(e, notification.id)
      );

      listItem.appendChild(title);
      listItem.appendChild(href);
      listItem.appendChild(content);
      if (notification.type === "friend_request") {
        listItem.appendChild(requestAcceptButton);
        listItem.appendChild(requestRejectButton);
      }
      listItem.appendChild(readButton);
      notificationList.appendChild(listItem);
    });
    setuplanguage();
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error getting notifications:", error);
  }
}

export async function readNotification(e, notificationId) {
  try {
    const response = await fetch(
      "http://localhost:8000/notification/read/" + notificationId + "/",
      {
        method: "PATCH",
        headers: {
          "Accept-Language": "tr",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      }
    );

    const data = await response.json();
    console.log(data);

    if (!response.ok) {
      throw new Error(data.message);
    }
    Toast({
      title: "Success",
      message: data.message,
      theme: "success",
    });
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error reading notification:", error);
  }
}

export async function acceptRequest(e, notificationId) {
  try {
    const response = await fetch(
      "http://localhost:8000/friend/accept-request/" + notificationId,
      {
        method: "GET",
        headers: {
          "Accept-Language": "tr",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      }
    );

    const data = await response.json();
    console.log(data);

    if (!response.ok) {
      throw new Error(data.error);
    }
    Toast({
      title: "Success",
      message: data.data,
      theme: "success",
    });
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error accepting request:", error);
  }
}
export async function rejectRequest(e, notificationId) {
  try {
    const response = await fetch(
      "http://localhost:8000/friend/reject-request/" + notificationId,
      {
        method: "GET",
        headers: {
          "Accept-Language": "tr",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      }
    );

    const data = await response.json();
    console.log(data);

    if (!response.ok) {
      throw new Error(data.error);
    }
    Toast({
      title: "Success",
      message: data.data,
      theme: "success",
    });
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error rejecting request:", error);
  }
}
