window.onload = function() {
    calculateCost();
    calculateTotal();
    $(".quantity-field").on("change", function() {
        if (parseInt(this.value) < 0) {
            this.value = 1;
        }
        if (parseInt(this.value) == 0) {
            $(this).closest(".slot-row").find(".delete-slot").click();
            return;
        }
        $.ajax({
            url: "/basket/update/" + this.id + "/?quantity=" + this.value,
            method: "GET",
            success: function(data) {
                console.log(data);
            }
        });
        calculateCost();
        calculateTotal();
    });
    $(".delete-slot").on("click", function() {
        $.ajax({
            url: "/basket/delete/" + this.id + "/",
            method: "GET",
            success: function(data) {
                console.log(data);
            }
        });
        $(this).closest(".slot-row").remove();
        calculateTotal();
    })
}

function calculateCost() {
    $(".slot-row").each(function() {
        var $price = parseFloat($(this).children(".product-price").text().replace(",", "."));
        var $quantity = parseInt($(this).find(".quantity-field").val());
        var $cost = ($price * $quantity).toFixed(2);
        $(this).children(".slot-cost").text($cost.replace(".", ","));
    })
}

function calculateTotal() {
    var $total = 0;
    $(".slot-cost").each(function() {
        $total += parseFloat($(this).text().replace(",", "."));
    })
    if ($total == 0) {
        $("#basket-detail").children("*").children("*").remove();
        $("#basket-detail").children("main").append($('<section class="empty-basket">Ваша корзина пуста</section>'));
        return;
    }
    $(".total-row").text("Итого: " + $total.toFixed(2).replace(".", ","));
}