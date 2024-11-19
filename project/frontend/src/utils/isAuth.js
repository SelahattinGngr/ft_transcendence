export function isAuth() {
  return !!localStorage.getItem("access_token");
}
