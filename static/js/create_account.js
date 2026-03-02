async function create_user() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const password_confirm = document.getElementById("password_confrim").value;
    const name = document.getElementById("name").value;
    const surname = document.getElementById("surname").value;
    const patronymic = document.getElementById("patronymic").value;
    const phone = document.getElementById("phone").value;
    const email = document.getElementById("email").value;
    const pasport = document.getElementById("pasport").value;
    const card = document.getElementById("card").value;

    const response = await fetch("/create_user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: username,
                password: password,
                password_confirm: password_confirm,
                name: name,
                surname: surname,
                patronymic: patronymic,
                phone: phone,
                email: email,
                pasport: pasport,
                card: card
            })
        });
    if (response.ok) {
        window.location.href = "/login";
    } else {
        const data = await response.json();
        alert(data.message)
    }
}