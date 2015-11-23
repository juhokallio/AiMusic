function compose() {
    console.log("Attempting composition");
    $.get("/composer/1/compose")
        .done(function (result) {
            console.log(result);
        });
}
