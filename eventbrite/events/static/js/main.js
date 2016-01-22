/**
 * Created by Saurabh on 14-Jan-16.
 */
$(document).ready(function () {
	$('input[name="categories"]').click(function() {
		var total=$(':checkbox:checked').length;
		
		$('#count').html(3 - total);
		if (total > 0 && total < 4) {
			$('#submit').prop('disabled', false);
		} else {
			$('#submit').prop('disabled',true);
		}
	});
	
});
