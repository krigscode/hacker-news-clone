jQuery(document).ready(function($) 
    {
	$(".vote_form").submit(function(e) 
		{
		    e.preventDefault(); 
		    var btn = $("button", this);
		    var l_id = $(".hidden_id", this).val();
		    btn.attr('disabled', true);
		    $.post("/vote/", $(this).serializeArray(),
			  function(data) {
				if(data["voteobj"]) {
					btn.text("-");
					// var a = $(".link_total_votes").val();
					// console.log(a);
					// $("#link_total_votes").val(parseInt(a)+1);
					} 
				else {
					btn.text("+");

				}
			  });
		    btn.attr('disabled', false);
		});
	
	
		$(".voting_button").click(function(){
			let button_val = $(this).text();
			let total_votes_as_string = $(this).siblings("p").html();
			if(button_val === "+"){
				let total_votes = parseInt(total_votes_as_string) + 1;
				$(this).siblings("p").text(total_votes.toString())
			} else {
				let total_votes = parseInt(total_votes_as_string) - 1;
				$(this).siblings("p").text(total_votes.toString())
			}
		});
	});
	
	