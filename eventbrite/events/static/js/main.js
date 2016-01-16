/**
 * Created by Saurabh on 14-Jan-16.
 */
$(document).ready(function () {
    console.log("ready!");
    $.get("https://www.eventbriteapi.com/v3/categories/?token=D5XL6OC6476ELPPFANDY", function (data) {
        $(data.categories).each(
            function (iter, val) {
                $(".result").append('<div class="checkbox event"> <label> <input type = "checkbox" name = "categories" value = ' + val['id'] + ' aria-label =' + val['id'] + '>' + val['short_name'] + '</label></div>');
            });
    });
});
