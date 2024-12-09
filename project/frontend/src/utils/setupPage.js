import { Toast } from "../components/toast.js";
import { moveToNext, otp } from "../pages/2fa/2fa.js";
import { sendFriendRequest } from "../pages/friend-request/friend.js";
import { aiGameSetup } from "../pages/games/ai/aiGameSetup.js";
import { AiGame } from "../pages/games/ai/game/aiGame.js";
import { Game } from "../pages/games/locale/game/game.js";
import { Tournament } from "../pages/games/locale-tournament/game/tournament.js";
import { localeTournamentSetup } from "../pages/games/locale-tournament/localeTournamentGameSetup.js";
import { localeGameSetup } from "../pages/games/locale/localeGameSetup.js";
import { homeActions } from "../pages/home/home.js";
import { getNotifications } from "../pages/notifications/notification.js";
import { loadProfile } from "../pages/profile/profile.js";
import { retryVerifyAccount } from "../pages/retry-verify-account/retry.js";
import { handleSignin, intraSignin } from "../pages/signin/signin.js";
import { handleSignup } from "../pages/signup/signup.js";
import { verificationCode } from "../pages/verify-account/verification.js";
import { authButtons } from "./authButtons.js";
import { authController, unAuthController } from "./isAuth.js";
import { fetchFriendRequests } from "../pages/friends-requests/requests.js";
import { fetchFriendsList } from "../pages/friends/friends.js";

export function setupPageActions(page) {
  try {
    authButtons();
    if (page === "") {
      // window.location.pathname kullanarak sayfa yolunu değiştirebilirsiniz.
      window.location.hash = "home";
    }
    if (page === "home") {
      homeActions();
    } else if (page === "signin") {
      unAuthController();
      submitHandler("signinForm", handleSignin);
      document
        .querySelector("#ecole-button-submit")
        .addEventListener("click", intraSignin);
    } else if (page === "2fa") {
      unAuthController();
      submitHandler("otpForm", otp);
    } else if (page === "signup") {
      unAuthController();
      submitHandler("signupForm", handleSignup);
    } else if (page === "profile") {
      loadProfile();
    } else if (page === "verify-account") {
      verificationCode();
    } else if (page === "not-found") {
      const randomNumber = Math.floor(Math.random() * 33) + 1;
      document.getElementById(
        "not-found-image"
      ).src = `/src/assets/errors/${randomNumber}.svg`;
    } else if (page === "retry-verify-account") {
      submitHandler("retryForm", retryVerifyAccount);
    } else if (page === "games/locale") {
      putRange("#ballSpeed", "#rangeValue");
      submitHandler("localeGamesForm", localeGameSetup);
    } else if (page === "games/locale-tournament") {
      putRange("#ballSpeed", "#rangeValue");
      submitHandler("localeTournamentGamesForm", localeTournamentSetup);
    } else if (page === "games/ai") {
      authController();
      putRange("#ballSpeed", "#rangeValue");
      putRange("#gameDifficulty", "#difficultyRangeValue");
      submitHandler("aiGamesForm", aiGameSetup);
    } else if (page === "games/ai/game") {
      try {
        new AiGame();
      } catch (error) {
        if (window.location.hash === "#games/ai/game") {
          console.error(error);
        }
      }
    } else if (page === "games/locale/game") {
      try {
        new Game();
      } catch (error) {
        if (window.location.hash === "#games/locale/game") {
          console.error(error);
        }
      }
    } else if (page === "games/locale-tournament/game") {
      try {
        new Tournament();
      } catch (error) {
        if (window.location.hash === "#games/locale-tournament/game") {
          console.error(error);
        }
      }
    } else if (page === "friend-request") {
      authController();
      submitHandler("friendRequestForm", sendFriendRequest);
    } else if (page === "friends") {
      authController();
      fetchFriendsList();
      document
        .querySelector("#refreshFriends")
        .addEventListener("click", fetchFriendsList);
    } else if (page === "friends-requests") {
      authController();
      fetchFriendRequests();
      document
        .querySelector("#updateRequests")
        .addEventListener("click", fetchFriendRequests);
    } else if (page === "notifications") {
      getNotifications();
      document
        .querySelector("#updateNotifications")
        .addEventListener("click", getNotifications);
    }
  } catch (error) {
    Toast({
      title: "Error",
      message: error.message,
      theme: "danger",
    });
    console.error("Error setting up page actions:", error);
  }
}
window.moveToNext = moveToNext;

function submitHandler(elementId, eventListener) {
  document.getElementById(elementId).addEventListener("submit", eventListener);
}

function putRange(querySelector, id) {
  document.querySelector(querySelector).addEventListener("input", (e) => {
    document.querySelector(id).innerHTML = e.target.value;
  });
}
