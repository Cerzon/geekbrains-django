window.onload = function() {
    $(".basket-action-link").on("click", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $.ajax({
            url: this.href,
            method: "GET",
            success: function(data) {
                $("#basket").children("dl").remove();
                $("#basket").children("p").remove();
                $("#basket").append(data);
            }
        })
    })
}
