async function toBasket() {
    const username = localStorage.getItem("username");
    const token = localStorage.getItem("token");
    window.location.href = `/basket/${username}/${token}`
}