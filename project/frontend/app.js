import { moveToNext } from "./src/pages/2fa/2fa.js";
import { getNotifications } from "./src/pages/notifications/notification.js";
import { active } from "./src/utils/active.js";
import { isvalidToken } from "./src/utils/isValidToken.js";
import {
  changelanguage,
  loadlanguage,
  setuplanguage,
} from "./src/utils/language.js";
import { setupPageActions } from "./src/utils/setupPage.js";
import { signout } from "./src/utils/signout.js";

window.changelanguage = changelanguage;
window.signout = signout;
window.getNotifications = getNotifications;
window.moveToNext = moveToNext;

document.addEventListener("DOMContentLoaded", async function () {
  isvalidToken();
  const hash = window.location?.hash?.slice(1) ?? "home";
  const page = hash.startsWith("profile/user") ? hash : hash.split("?")[0];
  await loadPage(page);
  active(page);
  loadlanguage();
});

window.addEventListener("hashchange", async function () {
  const hash = window.location?.hash?.slice(1) ?? "home";
  const page = hash.startsWith("profile/user") ? hash : hash.split("?")[0];
  await loadPage(page);
  active(page);
});

async function loadPage(page) {
  try {
    // TODO: window.location.pathname kullanarak sayfa yolunu değiştirebilirsiniz.
    if (page === "") {
      page = "home";
      window.location.hash = "#home";
    }
    const filePath = `/src/pages/${page.split("?")[0]}/`;
    const response = await fetch(filePath);
    if (!response.ok) {
      throw new Error("Page not found");
    }
    const html = await response.text();
    document.getElementById("app").innerHTML = html;
    setupPageActions(page);
    await setuplanguage();
  } catch (error) {
    loadPage("not-found");
    console.error("Error loading page:", page);
    console.error("Error loading error:", error);
  }
}
