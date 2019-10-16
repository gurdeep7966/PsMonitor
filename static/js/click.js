 jQuery(document).ready(function($) {
    $(".clickable").click(function() {
       alert($(this).data("href"));
        window.location = $(this).data("href");
    });
});