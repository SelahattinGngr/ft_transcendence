import { Toast } from "../../components/toast.js";
import { getLanguage } from "../../utils/language.js";

export async function fetchFriendsList() {
  try {
    const response = await fetch(
      "http://localhost:8000/api/user/list_friends",
      {
        method: "GET",
        headers: {
          "Accept-Language": getLanguage(),
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      }
    );

    const { data, error } = await response.json();
    if (!response.ok) {
      throw new Error(error);
    }
    const friendsList = document.getElementById("friendsList");
    friendsList.innerHTML = "";

    if (data.friends_list && data.friends_list.length > 0) {
      data.friends_list.forEach((friend) => {
        const listItem = document.createElement("li");
        listItem.classList.add("list-group-item");

        listItem.innerHTML = `
          <strong>${friend.username}</strong>
          <a href="/profile/${friend.username}" class="view-profile" target="_blank">Profili Gör</a>
          `;

        friendsList.appendChild(listItem);
      });
    } else {
      const noFriendsItem = document.createElement("li");
      noFriendsItem.classList.add("list-group-item");
      noFriendsItem.textContent = "Arkadaş listenizde kimse yok.";
      friendsList.appendChild(noFriendsItem);
    }
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
  }
}
