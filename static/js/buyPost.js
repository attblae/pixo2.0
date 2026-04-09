async function buying() {
    if (window.confirm(`BUY an art \n Is your card correct? \n 1234123412341234`)) {
        window.alert("You have bought the art!!!")
    } else {
        card = window.prompt("Enter your valid card:")
        if (card) {
            window.alert("You have bought the art!!!")
        }
    }
}