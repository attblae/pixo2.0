document.getElementById('file').onchange = function(e) {
    document.querySelector('.custom-file-upload').innerText = e.target.files[0].name || 'Choose file';
};

async function upload() {
    const token = localStorage.getItem("token");
    const price = document.getElementById("price").value;
    const title = document.getElementById("title").value;
    const file = document.getElementById("file").files[0];

    if (!token) {
        window.location.href = "/login";
        }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("token", token);
    formData.append("price", price);
    formData.append("title", title);
    
    const response = await fetch("/uploading", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        if (window.confirm("Do you want to post new art?")){
            window.location.href = "/post";
        } else {
            window.location.href = "/catalog";
        }
    } else {
        const data = await response.json();
        alert(data.message);
    }
}