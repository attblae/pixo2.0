async function postDeleting(button) {
    const token = localStorage.getItem("token");
    const url = button.dataset.url;

    const response = await fetch("/delete_from_basket", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            access_token: token,
            link: url
        })
    });

    if (response.ok) {
    const username = localStorage.getItem("username");
    const token = localStorage.getItem("token")
    window.location.href = `/basket/${username}/${token}`
    }
}