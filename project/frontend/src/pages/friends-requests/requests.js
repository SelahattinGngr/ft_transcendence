export async function fetchFriendRequests() {
  const response = await fetch(
    "http://localhost:8000/api/friend/list-friends-request/",
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
                        <button class="btn btn-success accept-request" data-id="${request.id}" onclick="acceptRequest(event, ${request.id})">Kabul Et</button>
                        <span>size bir arkadaşlık isteği gönderdi.</span>
                        <button class="btn btn-danger reject-request" data-id="${request.id}" onclick="rejectRequest(event, ${request.id})">Reddet</button>
                        <a href="/#profile/user?${request.sender_username}" class="view-profile">Profilini Gör</a>
                    `;

      friendsRequestLists.appendChild(listItem);
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
  const response = await fetch(
    `http://localhost:8000/api/friend/accept-friend-request/${id}/`,
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
}

export async function rejectRequest(e, id) {
  e.preventDefault();
  const response = await fetch(
    `http://localhost:8000/api/friend/reject-request/${id}/`,
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
}
