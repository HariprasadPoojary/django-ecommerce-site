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

// ? Add to cart from Store Page, Increase or Decrease/Remove item from Cart Page
// Get list of all products
let products = document.querySelectorAll(".add-cart");

async function updateCartOrder(productId, productAction) {
	console.log("User is authenticated, sending data..");

	const url = "/update_item/";
	let data = {
		productid: productId,
		action: productAction,
	};
	const response = await sendAJAX("POST", url, csrftoken, data); //*  csrftoken from main.html
	return response;
}

function addCookieItem(productId, productAction) {
	console.log("User not authenticated");
	if (productAction === "add") {
		if (cart[productId] == undefined) {
			cart[productId] = { quantity: 1 };
		} else {
			cart[productId]["quantity"] += 1;
		}
	}

	if (productAction === "remove") {
		cart[productId]["quantity"] -= 1;

		if (cart[productId]["quantity"] <= 0) {
			console.log("Item must be deleted");
			delete cart[productId];
		}
	}

	//* set cookie
	setCookie(cart);

	console.log("Cart:", cart);
}

for (let item of products) {
	item.addEventListener("click", function () {
		let productId = this.dataset.product;
		let productAction = this.dataset.action;
		console.log(`Product ID: ${productId}, Action: ${productAction}`);

		// Check if User is authenticated
		if (user === "AnonymousUser") {
			addCookieItem(productId, productAction);
		} else {
			updateCartOrder(productId, productAction).then((res) => {
				console.log(res);
			});
			location.reload();
		}
	});
}

//? Checkout Page Operations

// Django variables
//-- check in checkout.html

// Add Event listener to the form
const formTag = document.querySelector("#form");
const submitBtnTag = document.querySelector("#form-button");
const paymentTag = document.querySelector("#payment-info");
const paymentBtnTag = document.querySelector("#make-payment");

async function submitFormData() {
	console.log("Payment Btn clicked");
	// User data object
	let userFormData = {
		name: null,
		email: null,
		total: cart_total,
	};
	let shippingData = {
		address: null,
		city: null,
		state: null,
		pincode: null,
	};
	// Fill values
	if (shipping != "False") {
		shippingData.address = formTag.address.value;
		shippingData.city = formTag.city.value;
		shippingData.state = formTag.state.value;
		shippingData.pincode = formTag.pincode.value;
	}
	if (user == "AnonymousUser") {
		userFormData.name = formTag.name.value;
		userFormData.email = formTag.email.value;
	}

	// Send Data
	let data = {
		form: userFormData,
		shipping: shippingData,
	};
	const formResponse = await sendAJAX(
		"POST",
		"/process_order/",
		csrftoken,
		data
	); //*  csrftoken from main.html
	return formResponse;
}

formTag.addEventListener("submit", function (e) {
	e.preventDefault();

	console.log("Form submitted");
	// hide submit button
	submitBtnTag.classList.add("hidden");
	// reveal payment option
	paymentTag.classList.remove("hidden");
});

paymentBtnTag.addEventListener("click", function () {
	submitFormData().then((res) => {
		console.log(res);
	});
	alert("Transaction Completed!");
	window.location.href = "/";
});
