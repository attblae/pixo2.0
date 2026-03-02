async function check_user() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const response = await fetch("/login_account", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token)
        window.location.href = "/";
    } else {
        const data = await response.json();
        alert(data.message);
    };
}