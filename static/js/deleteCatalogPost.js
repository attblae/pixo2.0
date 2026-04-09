async function postDeleting(button) {
    const token = localStorage.getItem("token");
    const url = button.dataset.url;
    
    const response = await fetch("/delete_from_catalog", {
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
    window.location.href = `/account/${username}`
    }
}