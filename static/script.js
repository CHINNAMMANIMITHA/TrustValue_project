document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form[onsubmit]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm("Are you sure?")) event.preventDefault();
    });
  });
});
