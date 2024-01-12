let serverBaseURL = "http://127.0.0.1:5000/";

$(document).ready(function () {
  console.log(likes);
  $(".like-button").each(function () {
    let cardId = $(this).parent().attr("id");
    if (likes.includes(cardId)) {
      $(this).toggleClass("clicked");
    }
  });

  $(".like-button").on("click", function () {
    let cardId = $(this).parent().attr("id");

    $(this).toggleClass("clicked");
    console.log(likes);
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
  });
});
