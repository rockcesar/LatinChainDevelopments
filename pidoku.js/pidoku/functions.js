$( document ).ready(function() {
    $('.timer').countimer({
			autoStart : false
			});
    
    const PiNetworkClient = window.PiNetwork;
    
    async function auth() {
        try {

            const user = await PiNetworkClient.Authenticate();
            
            $( "#button_click" ).click(function() {
		if(parseFloat($("#pi_donate").val()) > 0)
		{
		    $("#button_click").prop( "disabled", true );
		    setTimeout(function ()
                    {
                        $("#button_click").prop( "disabled", false );
                    }, 10000);
                    transfer();
		}
            });
            //alert('Hello ' + user.username);
        } catch (err) {
            //alert(err);
            // Not able to fetch the user
        }
    }

    async function transfer() {
        try {
            //alert($("#pi_donate").val());
            const transferRequest = await PiNetworkClient.RequestTransfer(parseFloat($("#pi_donate").val()), "Donation to Sudoku");
            //if(transferRequest.status == "failed" || transferRequest.status == "succeeded")
	    $("#button_click").prop( "disabled", false );
            //alert(transferRequest.status);
        } catch(err) {
            //alert(err);
            // Technical problem (eg network failure). Please try again
        }
    }

    auth();
    
    $(".numeric-decimal").on("keypress keyup blur",function (event) {
        //this.value = this.value.replace(/[^0-9\.]/g,'');
        //$(this).val($(this).val().replace(/[^0-9\.]/g,''));
        if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
            event.preventDefault();
        }
    });
    
    $(".numeric").on("keypress keyup blur",function (event) {
        var val = $(this).val().replace(/[^\d].+/, "");
        if(val.length > 1)
            val = val.substring(0, 1);
        $(this).val(val);
        if ((event.which < 48 || event.which > 57)) {
            event.preventDefault();
        }
    });
    
    $(".sudoku-list").on("keypress keyup blur",function (event) {
        //this.value = this.value.replace(/[^0-9\.]/g,'');
        //$(this).val($(this).val().replace(/[^0-9\.]/g,''));
        if ((event.which != 46) && (event.which < 49 || event.which > 57)) {
            event.preventDefault();
        }
    });
    
    
});
