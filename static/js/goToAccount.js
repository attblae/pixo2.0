async function toAccount() {
    const username = localStorage.getItem("username");
    const token = localStorage.getItem("token")
    window.location.href = `/account/${username}/${token}`
}