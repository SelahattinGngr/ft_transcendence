import { isAuth } from "./isAuth.js";

export function authButtons() {
  const authContainer = document.querySelector("#auth");
  const profileDropdown = document.querySelector("#profile-dropdown");

  if (isAuth()) {
    authContainer.classList.remove("d-flex");
    authContainer.classList.add("d-none");

    profileDropdown.classList.remove("d-none");
    profileDropdown.classList.add("d-flex");
  } else {
    profileDropdown.classList.remove("d-flex");
    profileDropdown.classList.add("d-none");

    authContainer.classList.remove("d-none");
    authContainer.classList.add("d-flex");
  }
}
