"use strict";
console.log("Hare Krishna!");

let products = document.querySelectorAll(".add-cart");

async function updateCartOrder(productId, productAction) {
	console.log("User is authenticated, sending data..");

	const url = "/update_item/";
	let data = {
		productid: productId,
		action: productAction,
	};
	try {
		const res = await fetch(url, {
			method: "POST",
			body: JSON.stringify(data),
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrftoken,
			},
		});
		let response = await res.json();
		return response;
	} catch (error) {
		throw error;
	}
}

for (let item of products) {
	item.addEventListener("click", async function () {
		let productId = this.dataset.product;
		let productAction = this.dataset.action;
		console.log(`Product ID: ${productId}, Action: ${productAction}`);

		// Check if User is authenticated
		if (user === "AnonymousUser") {
			console.log("User is not authenticated");
		} else {
			let response = await updateCartOrder(productId, productAction);
			location.reload();
			console.log(response);
		}
	});
}
