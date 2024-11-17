// signin sayfasında form işlemi yapılacak

import { loadProfile } from "./src/pages/profile/profile.js";

document.addEventListener("DOMContentLoaded", async function () {
    const page = window.location.hash.slice(1) || "home.html";
    await loadPage(page);
});

window.addEventListener("hashchange", async function () {
    const newPage = window.location.hash.slice(1) || "home.html";
    await loadPage(newPage);
});

function handleEvent(event) {
    event.preventDefault(); // Tarayıcı varsayılan davranışını engelle
    const newPage = event.target.getAttribute("href").slice(1);
    window.location.hash = newPage; // Hash'i güncelle
}

async function loadPage(page) {
    await fetch(`/src/pages/${page}`)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Page not found");
            }
            return response.text();
        })
        .then((html) => {
            document.getElementById("app").innerHTML = html;

            // Sayfaya özel işlemler
            switch (page) {
                case "src/pages/profile":
                    loadProfile();
                    break;
                case "src/pages/signin":
                    document.querySelector("form").addEventListener("submit", handleSignin);
                    break;
                case "src/pages/signup":
                    document.querySelector("form").addEventListener("submit", handleSignup);
                    break;
            }

            // Linklere dinleyici ekle
            setupNavigation();
        })
        .catch((error) => {
            console.error("Error loading page:", error);
        });
}

function setupNavigation() {
    const allhref = document.querySelectorAll("a");
    allhref.forEach((element) => {
        element.addEventListener("click", handleEvent);
    });
}



async function handleSignin(event) {
    event.preventDefault();
    const signin = document.getElementById("signinUsername").value;
    const password = document.getElementById("signinPassword").value;

    try {
        const response = await fetch("http://localhost:8000/auth/signin/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept-Language": "tr",
            },
            body: JSON.stringify({ signin, password }),
        });

        if (response.ok) {
            const data = await response.json();

            localStorage.setItem("access_token", data.data.access_token.token);
            localStorage.setItem("username", data.data.username);

            alert("Sign in successful!");
            navigateTo("homepage.html");
        } else {
            const errorData = await response.json();
            alert("Sign in failed: " + errorData.message);
        }
    } catch (error) {
        console.error("Error during sign in:", error);
    }
}


async function logout() {
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
        alert("No active session found.");
        navigateTo("signin.html");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/auth/signout/", {
            method: "GET",
            headers: {
                "Accept-Language": "tr",
                Authorization: `Bearer ${accessToken}`,
            },
        });

        if (response.ok) {
            alert("Logout successful!");
            localStorage.clear(); // Tüm localStorage'ı temizle
            navigateTo("signin.html"); // Giriş sayfasına yönlendir
        } else {
            const errorData = await response.json();
            console.error("Logout failed:", errorData.message);
            alert("Logout failed: " + (errorData.message || "Unknown error"));
        }
    } catch (error) {
        console.error("Error during logout:", error);
        alert("Error during logout. Please try again.");
    }
}


async function handleSignup(event) {
    event.preventDefault();
    const username = document.getElementById("signupUsername").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    const first_name = document.getElementById("signupFirstName").value;
    const last_name = document.getElementById("signupLastName").value;
    const avatar_url = document.getElementById("signupAvatarUrl").value;

    try {
        const response = await fetch("http://localhost:8000/auth/signup/", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Accept-Language": "tr"
            },
            body: JSON.stringify({ username, email, password, first_name, last_name, avatar_url }),
        });

        if (response.ok) {
            const data = await response.json();
            alert("Sign up successful!");
            await loadPage("signin.html");
        } else {
            const errorData = await response.json();
            alert("Sign up failed: " + errorData.message);
        }
    } catch (error) {
        console.error("Error during sign up:", error);
    }
}

function navigateTo(page) {
    loadPage(page)
        .then(() => {
            if (page === "profile.html") {
                loadProfile();
            }
        })
        .catch((error) => {
            console.error("Navigation error:", error);
        });
}


