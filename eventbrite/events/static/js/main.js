/**
 * Created by Saurabh on 14-Jan-16.
 */
$(document).ready(function () {
	$('input[name="categories"]').click(function() {
		var total=$(':checkbox:checked').length;
		console.log(total);
	});
	
});
