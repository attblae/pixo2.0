document.addEventListener("DOMContentLoaded", async function () {
const token = localStorage.getItem("token");

console.log('dfijposfpjosdfpoj')

if (!token) {
    window.location.href = "/login";
} else {
    const response = await fetch("/check_token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            access_token: token
        })
    });
    if (!response.ok) {
        localStorage.removeItem("token");
        window.location.href = "/login";
    } else {
        const data = await response.json();
        localStorage.setItem("username", data.username)
    }
}

});