async function toAccount() {
    const username = localStorage.getItem("username");
    window.location.href = `/account/${username}`
}