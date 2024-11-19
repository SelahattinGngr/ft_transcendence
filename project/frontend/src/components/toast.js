export function Toast({ title = "Error", message, theme = "warning" }) {
  console.log("Toast message:", message);
  const toastContainer = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.id = "liveToast";
  toast.classList.add("toast");
  toast.classList.add(`text-bg-${theme}`);
  toast.role = "alert";
  toast.ariaLive = "assertive";
  toast.ariaAtomic = "true";
  toast.setAttribute("data-bs-theme", "dark");
  toast.innerHTML = `
    <div class="toast-header">
      <strong class="me-auto">${title}</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
        ${message}
    </div>        
    `;
  toastContainer.appendChild(toast);
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
  toastBootstrap.show();
}
