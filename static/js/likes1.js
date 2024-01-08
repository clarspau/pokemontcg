// Filename: likeHandler.js

// Base URL for the server
const serverBaseURL = "http://127.0.0.1:5000/";

// Function to set up initial like state
function setupInitialLikes() {
     $(".like-button").each(function () {
          let cardId = $(this).parent().attr("id");
          if (likes.includes(cardId)) {
               $(this).toggleClass("clicked");
          }
     });
}

// Function to handle like button clicks
function handleLikeButtonClick() {
     $(".like-button").on("click", function () {
          let cardId = $(this).parent().attr("id");
          $(this).toggleClass("clicked");

          console.log(likes);

          // Send like status to the server
          $.ajax({
               url: `${serverBaseURL}addlike`,
               method: "POST",
               data: JSON.stringify({
                    card_id: cardId,
               }),
               contentType: "application/json",
               success: function (response) {
                    console.log(response);
                    // Use API data here if needed
               },
               error: function (error) {
                    console.error("Error:", error);
               },
          });
     });
}

// Document ready event
$(document).ready(function () {
     // Initialize likes
     setupInitialLikes();

     // Set up event listener for like button clicks
     handleLikeButtonClick();
});
