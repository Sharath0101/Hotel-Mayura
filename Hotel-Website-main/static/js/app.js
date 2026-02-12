// Function to validate the Contact Us form
function validateContactForm() {
    const name = document.forms["contactForm"]["name"].value;
    const email = document.forms["contactForm"]["email"].value;
    const phone = document.forms["contactForm"]["phone"].value;
    const message = document.forms["contactForm"]["message"].value;

    if (name === "" || email === "" || phone === "" || message === "") {
        alert("All fields must be filled out.");
        return false;
    }
    return true;
}

// Function to validate the Room Booking form
function validateRoomBookingForm() {
    const name = document.forms["roomBookingForm"]["name"].value;
    const phone = document.forms["roomBookingForm"]["phone"].value;
    const date = document.forms["roomBookingForm"]["date"].value;
    const roomType = document.forms["roomBookingForm"]["roomType"].value;

    if (name === "" || phone === "" || date === "" || roomType === "") {
        alert("All fields must be filled out.");
        return false;
    }
    return true;
}

// Function to handle Room Booking selection
function selectRoom(room) {
    const roomDetails = document.getElementById("roomDetails");
    const roomPrice = document.getElementById("roomPrice");

    roomDetails.textContent = `You have selected the ${room.name}.`;
    roomPrice.textContent = `Price: $${room.price}/night`;

    // Store the selected room in localStorage or sessionStorage
    sessionStorage.setItem("selectedRoom", JSON.stringify(room));
}

// Function to handle Table Reservation for Restaurant
function reserveTable() {
    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;

    if (name === "" || phone === "" || date === "" || time === "") {
        alert("Please fill all the fields.");
        return;
    }

    alert(`Reservation Confirmed!\nName: ${name}\nPhone: ${phone}\nDate: ${date}\nTime: ${time}`);
    document.getElementById("reservationForm").reset();
}

// Function to handle Party Hall Booking
function reservePartyHall() {
    const name = document.getElementById("eventName").value;
    const phone = document.getElementById("eventPhone").value;
    const date = document.getElementById("eventDate").value;
    const time = document.getElementById("eventTime").value;
    const details = document.getElementById("eventDetails").value;

    if (name === "" || phone === "" || date === "" || time === "") {
        alert("Please fill all the fields.");
        return;
    }

    alert(`Party Hall Reservation Confirmed!\nEvent Name: ${name}\nPhone: ${phone}\nDate: ${date}\nTime: ${time}\nDetails: ${details}`);
    document.getElementById("partyHallForm").reset();
}

// Function to handle Feedback form submission
function submitFeedback() {
    const customerId = document.getElementById("customerId").value;
    const message = document.getElementById("message").value;

    if (message === "") {
        alert("Please provide feedback.");
        return;
    }

    alert("Thank you for your feedback!");

    // Store feedback in the local storage (for demo purposes)
    const feedbackData = {
        customerId: customerId,
        message: message,
    };

    let feedbacks = JSON.parse(localStorage.getItem("feedbacks")) || [];
    feedbacks.push(feedbackData);
    localStorage.setItem("feedbacks", JSON.stringify(feedbacks));

    document.getElementById("feedbackForm").reset();
}

// Function to show Reviews dynamically (for the reviews page)
function loadReviews() {
    const reviews = [
        { name: "John Doe", section: "Room", rating: 5, comment: "The room was amazing! Great experience!" },
        { name: "Sarah Smith", section: "Restaurant", rating: 4, comment: "Good food, but the service was slow." },
        { name: "James Johnson", section: "Party Hall", rating: 5, comment: "Perfect venue for my wedding. Excellent service!" },
    ];

    const reviewsContainer = document.getElementById("reviewsContainer");
    reviewsContainer.innerHTML = ""; // Clear the existing reviews

    reviews.forEach((review) => {
        const reviewElement = document.createElement("div");
        reviewElement.classList.add("bg-white", "p-6", "rounded-lg", "shadow-lg", "mb-4");

        reviewElement.innerHTML = `
            <h3 class="text-2xl font-semibold text-gray-900">${review.name} - ${review.rating} Stars</h3>
            <p class="mt-4 text-lg text-gray-600">"${review.comment}"</p>
            <p class="mt-2 font-semibold text-gray-800">Review for: ${review.section}</p>
        `;

        reviewsContainer.appendChild(reviewElement);
    });
}

// Function to handle the submission of the contact form (for demonstration purposes)
document.getElementById("contactFormSubmit").addEventListener("click", function(event) {
    event.preventDefault();
    if (validateContactForm()) {
        alert("Thank you for contacting us!");
        document.getElementById("contactForm").reset();
    }
});

// Function to handle the submission of the room booking form (for demonstration purposes)
document.getElementById("roomBookingSubmit").addEventListener("click", function(event) {
    event.preventDefault();
    if (validateRoomBookingForm()) {
        alert("Your room booking has been confirmed!");
        document.getElementById("roomBookingForm").reset();
    }
});

// Function to initialize the page (to load reviews, etc.)
document.addEventListener("DOMContentLoaded", function() {
    loadReviews();
});

