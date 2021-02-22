"use strict";
console.log("Hare Krishna!");

//? Send AJAX request with fetch
const sendAJAX = async function (method, url, csrf, data) {
	try {
		const res = await fetch(url, {
			method: method,
			body: JSON.stringify(data),
			headers:
				method !== "GET"
					? {
							"Content-Type": "application/json",
							"X-CSRFToken": csrf,
					  }
					: {},
		});
		if (res.status >= 400) {
			// Convert response to JavaScript object
			const errResponse = await res.json();
			const err = new Error("Something went wrong!!");
			err.data = errResponse;
			throw err;
		}
		let dataResponse;
		if (method !== "DELETE") dataResponse = await res.json();
		return dataResponse;
	} catch (error) {
		throw error;
	}
};

// Get list of all products
let products = document.querySelectorAll(".add-cart");

async function updateCartOrder(productId, productAction) {
	console.log("User is authenticated, sending data..");

	const url = "/update_item/";
	let data = {
		productid: productId,
		action: productAction,
	};
	const token = csrftoken; // token from main.html
	const response = await sendAJAX("POST", url, token, data);
	console.log(response);
	return response;
}

for (let item of products) {
	item.addEventListener("click", function () {
		let productId = this.dataset.product;
		let productAction = this.dataset.action;
		console.log(`Product ID: ${productId}, Action: ${productAction}`);

		// Check if User is authenticated
		if (user === "AnonymousUser") {
			console.log("User is not authenticated");
		} else {
			updateCartOrder(productId, productAction);
			location.reload();
		}
	});
}
