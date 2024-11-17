export async function loadProfile() {
    const username = localStorage.getItem("username");
    if (!username) {
        console.error("No username found in localStorage");
        return;
    }

    try {
        const response = await fetch(`http://localhost:8000/user/${username}`, {
            method: "GET",
            headers: {
                "Accept-Language": "tr",
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
        });

        if (response.ok) {
            const data = (await response.json()).data;

            // Profil bilgilerini sayfaya yükle
            document.getElementById("profile-avatar").src =
                data.avatar_url || "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50";
            console.log(data.avatar_url);
            document.getElementById("profile-username").textContent = data.username;
            document.getElementById("profile-bio").textContent = data.bio || "Bio not provided";
            document.getElementById("profile-firstname").textContent = data.first_name;
            document.getElementById("profile-lastname").textContent = data.last_name;
            document.getElementById("profile-email").textContent = data.email;
        } else {
            const errorData = await response.json();
            alert("Failed to load profile: " + errorData.message);
        }
    } catch (error) {
        console.error("Error loading profile:", error);
    }
}
