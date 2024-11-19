export function active(page) {
  document.querySelector(".active")?.classList.remove("active");
  document.querySelector(`a[href="#${page}"]`)?.classList.add("active");
}
