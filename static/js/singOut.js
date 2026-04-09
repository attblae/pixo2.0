async function singOut() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
};