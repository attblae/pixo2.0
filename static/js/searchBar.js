async function search() {
    const searchInfo = document.getElementById("search").value;
    if (!searchInfo) {
        window.location.href = '/catalog'
    };
    const url = `/catalog?search=${encodeURIComponent(searchInfo)}`;
    window.location.href = url;
}