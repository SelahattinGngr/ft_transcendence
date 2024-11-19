import { isAuth } from "../../utils/isAuth.js";

export function homeActions() {
  if (isAuth()) {
    document.querySelector("#with-auth").classList.replace("d-grid", "d-none");
    document
      .querySelector("#with-auth")
      .classList.replace("d-md-flex", "d-none");
    return;
  }
  document.querySelector("#game-btn").classList.replace("d-grid", "d-none");
  document.querySelector("#game-btn").classList.replace("d-md-flex", "d-none");
}
