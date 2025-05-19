function addToCart(productId) {
    const productName = document.querySelector(".details-section h1").textContent;
    const sku = document.querySelector(".details-section p:nth-of-type(1)").textContent.replace("SKU: ", "").trim();
    const price = document.querySelector(".price").textContent.replace("Rs.", "").trim();
    const imageUrl = document.querySelector(".image-section img").src;

    console.log("📤 Sending Data:", { sku, productName, price, imageUrl });

    fetch("/add_to_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            sku: sku, 
            product_name: productName,
            price: parseFloat(price),
            image_url: imageUrl
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server Response:", data);
        alert(data.message);
        updateCartCount();
    })
    .catch(error => console.error(" Error:", error));
}
function updateCartCount() {
    fetch("/cart_count")
        .then(response => response.json())
        .then(data => {
            document.getElementById("cart-count").textContent = data.count;
        })
        .catch(error => console.error("Error fetching cart count:", error));
}


document.addEventListener("DOMContentLoaded", updateCartCount);

