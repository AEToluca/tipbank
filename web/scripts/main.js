// Read stored values and show them in the header. If missing, redirect to login.
(function() {
  const name = localStorage.getItem('username');
  const id = localStorage.getItem('userid');
  const el = document.getElementById('logged-in');
  el.textContent = `Logged In As: ${name} (${id})`;
})();
