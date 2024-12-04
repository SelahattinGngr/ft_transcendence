const languageTitle = document.querySelector("#langDropdown");

export async function setuplanguage() {
  let language = localStorage.getItem("language");
  if (!language) {
    language = "TR";
    localStorage.setItem("language", language);
  }
  const response = await fetch(`/src/languages/${language}.json`);
  if (!response.ok) {
    changelanguage("TR");
    return;
  }
  const json = await response.json();
  const elements = document.querySelectorAll("[data-lang-path]");
  elements.forEach((element) => {
    const path = element.getAttribute("data-lang-path");
    const keys = path.split(".");
    let value = json;
    keys.forEach((key) => {
      value = value ? value[key] : undefined;
    });

    if (value !== undefined) {
      element.innerHTML = value;
    }
  });
}

export function loadlanguage() {
  const language = localStorage.getItem("language");
  if (language) {
    languageTitle.innerHTML = language;
  } else {
    localStorage.setItem("language", "TR");
  }
}

export function changelanguage(language) {
  localStorage.setItem("language", language);
  languageTitle.innerHTML = language;
  setuplanguage();
}

export const getLanguage = () => localStorage.getItem("language");
