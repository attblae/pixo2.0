async function toBasket() {
    const username = localStorage.getItem("username");
    window.location.href = `/basket/${username}`
}