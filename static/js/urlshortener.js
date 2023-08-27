$(document).ready(function () {
  $("#random").click(function () {
    const characters =
      "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let randomId = "";

    for (let i = 0; i < 10; i++) {
      const randomIndex = Math.floor(Math.random() * characters.length);
      randomId += characters.charAt(randomIndex);
    }
    $("#short_link").val(randomId);
  });
  $(document).on("submit", "#post-form", function (e) {
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: "/urlshortener/create",
      data: {
        link: $("#link").val(),
        short_link: $("#short_link").val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (data) {
        $("h2").html(data);
      },
    });
  });
});
