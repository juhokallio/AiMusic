function compose() {
    var newComposition = $('<div><img src="static/images/waiting.gif"/></div>');
    $("#composition-list").append(newComposition);
    $.get("/composer/1/compose")
        .done(function (result) {
            newComposition.html(result);
        });
}
