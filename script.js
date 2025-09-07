function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  // demo login credentials (you can change)
  const validUsername = "Admin";
  const validPassword = "1234";

  if (username === validUsername && password === validPassword) {
    // redirect to home page
    window.location.href = "home.html";  
  } else {
    alert("Invalid username or password");
  }
}


function goToCompanies(area) {
    if (!area) {
        alert("Please select an area.");
        return;
    }
    const v = area.toLowerCase();
    if (v === "hyderabad") window.location.href = "companies_hyderabad.html";
    else if (v === "bangalore") window.location.href = "companies_bangalore.html";
    else if (v === "chennai") window.location.href = "companies_chennai.html";
    else alert("Company listings for this area are not available yet.");
}