let serverBaseURL = "http://127.0.0.1:5000/";

$(document).ready(function () {
  // This toggles the clicked class for each like button based on the database
  $(".like-button").each(function () {
    let cardId = $(this).parent().attr("id");
    if (likes.includes(cardId)) {
      $(this).toggleClass("clicked");
    }
  });

  // This is for when a like button clicked, if its already clicked, then it removes it from the DB. if it isnt, it turns it red and adds it to the DB
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
          // use api data here, if needed
        },
      });
    } else {
      let index = likes.indexOf(cardId);
      if (index !== -1) {
        console.log(likes);
        console.log(typeof likes);
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
          // use api data here, if needed
        },
      });
    }

    $(this).toggleClass("clicked");
    console.log(likes);
  });
});
