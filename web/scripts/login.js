document.addEventListener("DOMContentLoaded", function () {
  const nameInput = document.getElementById("fname");
  const numberInput = document.getElementById("id");
  const button = document.getElementById("login");

  button.addEventListener("click", function () {
    const naValue = nameInput.value.trim();
    const nuValue = numberInput.value.trim();

    localStorage.setItem("username", naValue);
    localStorage.setItem("userid", nuValue);

    
    window.location.href = "main.html";
  });
});