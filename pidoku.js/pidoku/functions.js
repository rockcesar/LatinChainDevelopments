$( document ).ready(function() {
    const PiNetworkClient = window.PiNetwork;
    
    async function auth() {
        try {

            const user = await PiNetworkClient.Authenticate();

            alert('Hello ' + user.username);
        } catch (err) {
            alert(err);
            // Not able to fetch the user
        }
    }

    async function transfer() {
        try {
            const transferRequest = await PiNetworkClient.RequestTransfer(3.14, "Demo transfer request");
            alert(transferRequest.status);
        } catch(err) {
            alert(err);
            // Technical problem (eg network failure). Please try again
        }
    }

    auth();

    $( "#button_click" ).click(function() {
        transfer();
    });
    
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
    
    
});
