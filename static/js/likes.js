let serverBaseURL = "http://127.0.0.1:5000/";
let likes = [];  // Define the array to store liked card IDs

$(document).ready(function () {
     // This toggles the clicked class for each like button based on the database
     $(".like-button").each(function () {
          let cardId = $(this).parent().attr("id");
          if (likes.includes(cardId)) {
               $(this).toggleClass("clicked");
          }
     });

     // This is for when a like button is clicked, if it's already clicked, then it removes it from the DB. If it isn't, it turns it red and adds it to the DB
     $(".like-button").on("click", function () {
          let cardId = $(this).parent().attr("id");
          let isClicked = $(this).hasClass("clicked");

          if (!isClicked) {
               likes.push(cardId);
               $.ajax({
                    url: `${serverBaseURL}addlike`,
                    method: "POST",
                    data: JSON.stringify({
                         card_id: cardId,
                    }),
                    contentType: "application/json",
                    success: function (response) {
                         console.log(response);
                         // Use API data here, if needed
                    },
                    error: function (error) {
                         console.error("Error adding like:", error);
                         // Handle errors, if needed
                    },
               });
          } else {
               let index = likes.indexOf(cardId);
               if (index !== -1) {
                    likes.splice(index, 1);
               }
               $.ajax({
                    url: `${serverBaseURL}deletelike`,
                    method: "POST",
                    data: JSON.stringify({
                         card_id: cardId,
                    }),
                    contentType: "application/json",
                    success: function (response) {
                         console.log(response);
                         // Use API data here, if needed
                    },
                    error: function (error) {
                         console.error("Error deleting like:", error);
                         // Handle errors, if needed
                    },
               });

               // Add this block to handle the removal of the card from the Liked Cards page
               if (window.location.href.includes('/likes')) {
                    $(this).parent().remove();  // Remove the card from the Liked Cards page
               }
          }

          $(this).toggleClass("clicked");
          console.log(likes);
     });
});
