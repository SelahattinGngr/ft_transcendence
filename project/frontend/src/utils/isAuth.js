export function isAuth() {
  return !!localStorage.getItem("access_token");
}

export function authController() {
  if (!isAuth()) {
    window.location.hash = "signin";
    throw new Error("You are not authorized to access this page.");
  }
}

export function unAuthController() {
  if (isAuth()) {
    window.location.hash = "home";
    throw new Error("You are already authorized.");
  }
}
