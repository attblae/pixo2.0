async function sendToBasket(button) {
        const token = localStorage.getItem("token");

            if (!token) {
                window.location.href = "/login";
               }

            const price = button.dataset.price;
            const url = button.dataset.url;

            console.log({
                access_token: token,
                link: url,
                price: price
            });

            const response = await fetch("/put_in_basket", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    access_token: token,
                    link: url,
                    price: price
                })
            });
            }