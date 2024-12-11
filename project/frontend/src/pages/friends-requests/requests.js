import { Toast } from "../../components/toast.js";

export async function fetchFriendRequests() {
  const response = await fetch(
    "https://k2m10s01.42kocaeli.com.tr:8080/myapi/friend/list-friends-request/",
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

  const friendsRequestLists = document.getElementById("friendsRequestLists");
  friendsRequestLists.innerHTML = "";

  if (data.data.friends_requests && data.data.friends_requests.length > 0) {
    data.data.friends_requests.forEach((request) => {
      const listItem = document.createElement("li");
      listItem.classList.add("list-group-item");

      listItem.innerHTML = `
                        <strong>${request.sender_username}</strong>
                        <button class="btn btn-success accept-request" data-id="${request.id}">Kabul Et</button>
                        <span>size bir arkadaşlık isteği gönderdi.</span>
                        <button class="btn btn-danger reject-request" data-id="${request.id}">Reddet</button>
                        <a href="/#profile/user?${request.sender_username}" class="view-profile">Profilini Gör</a>
                    `;

      friendsRequestLists.appendChild(listItem);
    });
    document.querySelector(".accept-request").addEventListener("click", (e) => {
      acceptRequest(e, e.target.dataset.id);
    });
    document.querySelector(".reject-request").addEventListener("click", (e) => {
      rejectRequest(e, e.target.dataset.id);
    });
  } else {
    const listItem = document.createElement("li");
    listItem.classList.add("list-group-item");
    listItem.textContent = "Henüz arkadaşlık isteğiniz yok.";
    friendsRequestLists.appendChild(listItem);
  }
}

export async function acceptRequest(e, id) {
  e.preventDefault();
  try {
    const response = await fetch(
      `https://k2m10s01.42kocaeli.com.tr:8080/myapi/friend/accept-request/${id}/`,
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
    fetchFriendRequests();
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
  }
}

export async function rejectRequest(e, id) {
  e.preventDefault();
  try {
    const response = await fetch(
      `https://k2m10s01.42kocaeli.com.tr:8080/myapi/friend/reject-request/${id}/`,
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
    fetchFriendRequests();
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
  }
}
