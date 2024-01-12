increaseButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
        event.preventDefault();
        const currentItem = event.target.closest(".cart-item");
        const cartItemId = currentItem.getAttribute("data-cart-item-id");

        
    });
});

decreaseButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
        event.preventDefault();
        const currentItem = event.target.closest(".cart-item");
        const cartItemId = currentItem.getAttribute("data-cart-item-id");

      
    });
});

function updateCartItemPrice(priceElement, pricePerItem, quantity) {
    const updatedPrice = (pricePerItem * quantity).toFixed(2);
    localStorage.setItem('product', JSON.stringify(updatedPrice));
    let total=JSON.parse(localStorage.getItem('product'))
    priceElement.textContent = "$" + updatedPrice;
}

