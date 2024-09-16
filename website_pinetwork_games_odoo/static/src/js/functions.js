var pi_user_id = "";
var pi_user_code = "";
var accessToken = "";
var passkey = "";
var amount = 0;
const Pi = window.Pi;
var startTime=new Date(), endTime=new Date(), seconds=0;
var unblocked = false;
var show_pi_ad_user = true;

function setConfirmUnload(on) {
    if(on)
    {
        //alert($("#notclose_message").text());
    }
     window.onbeforeunload = on ? unloadMessage : null;
}

function setConfirmUnloadPoints(on) {
     window.onbeforeunload = on ? unloadMessage : null;
}

function unloadMessage() {
    return true;
}

function start() {
  startTime = new Date();
};

function end() {
  endTime = new Date();
  var timeDiff = endTime - startTime; //in ms
  // strip the ms
  timeDiff /= 1000;

  // get seconds 
  seconds = Math.round(timeDiff);
}

function set_points(points) {
    if(pi_user_id != "" && pi_user_code != "")
    {
        var data = {
            'pi_user_id': pi_user_id,
            'pi_user_code': pi_user_code,
            'points': points,
            'passkey': passkey,
            'accessToken': accessToken,
            'csrf_token': odoo.csrf_token,
        };
        //$.ajaxSetup({async: false});
        setConfirmUnloadPoints(true);
        return $.post( "/pi-points", data).done(function(data) {
            setConfirmUnloadPoints(false);
            data = JSON.parse(data);
            if(data.result && points > 0)
                alert("+" + points + $("#points_message").text());
        }).fail(function() {
            setConfirmUnloadPoints(false);
        });
    }
}

function get_user(donation) {
    if(pi_user_id != "" && pi_user_code != "")
    {
        var data = {
                    'pi_user_id': pi_user_id,
                    'pi_user_code': pi_user_code,
                    'accessToken': accessToken,
                    'csrf_token': odoo.csrf_token,
                };
        //$.ajaxSetup({async: false});
        return $.post( "/get-user", data).done(function(data) {
            data = JSON.parse(data);
            if(data.result)
            {
                if(data.complete_found)
                    alert($("#payment_message").text());
                    
                passkey=data.passkey;
                if(data.unblocked)
                {
                    unblocked = data.unblocked;
                    if(donation)
                        alert($("#unblocked_message").text());
                }
                show_pi_ad_user = data.show_pi_ad;
            }
        }).fail(function() {
            
        });
    }
}

async function showPiAds(Pi) {
    try {
        const isAdReadyResponse = await Pi.Ads.isAdReady("interstitial");
                                
        if (isAdReadyResponse.ready === false) {
            await Pi.Ads.requestAd("interstitial");
        }
        
        const showAdResponse = await Pi.Ads.showAd("interstitial");
        
        if(showAdResponse.result == "AD_CLOSED")
        {
            if(pi_user_id != "" && pi_user_code != "")
            {
                var data = {
                            'pi_user_id': pi_user_id,
                            'pi_user_code': pi_user_code,
                            'accessToken': accessToken,
                            'csrf_token': odoo.csrf_token,
                        };
                //$.ajaxSetup({async: false});
                return $.post( "/set-pi-ad-datetime", data).done(function(data) {
                    data = JSON.parse(data);
                    if(data.result)
                    {
                    }
                }).fail(function() {
                    
                });
            }
        }
    } catch (err) {
        //alert(err);
        // Not able to fetch the user
    }
}

$( document ).ready(function() {
    $(document).ajaxStop(function() {
                $("#loading_section").hide();
                $("#loading_word").hide();
            });
    
    Pi.init({ version: "2.0", sandbox: $("#sandbox").val() });
    //alert(PiNetworkClient);
    
    amount = $("#amount").val();

    async function auth() {
        $("#loading_section").show();
        $("#loading_word").show();
                                
        setTimeout(function() {
            $("#loading_section").hide();
            $("#loading_word").hide();
        }, 5000);
        
        try {
            const nativeFeaturesList = await Pi.nativeFeaturesList();
            const adNetworkSupported = nativeFeaturesList.includes("ad_network");
            
            if(!adNetworkSupported)
                alert("Update Pi Browser version, please!.");
            
            // Identify the user with their username / unique network-wide ID, and get permission to request payments from them.
            const scopes = ['username', 'payments', 'wallet_address'];
            function onIncompletePaymentFound(payment) {
                
                try {
                    var txid = payment.transaction.txid;
                } catch (e) {
                    var txid = "";
                }
                
                var data = {
                        'action': 'complete',
                        'paymentId': payment.identifier,
                        'txid': txid,
                        'app_client': 'auth_example',
                        'csrf_token': odoo.csrf_token,
                        'accessToken': accessToken,
                        'pi_user_code': pi_user_code,
                        'pi_user_id': pi_user_id,
                    };
                
                setConfirmUnloadPoints(true);
                return $.post( "/pi-api", data).done(function(data) {
                    setConfirmUnloadPoints(false);
                    $("#button_click").prop( "disabled", false );
                    try {
                        data = JSON.parse(data);
                        if(data.result && data.completed)
                        {
                            alert($("#payment_message").text());
                        }
                    } catch (e) {
                    }
                }).fail(function() {
                    setConfirmUnloadPoints(false);
                    $("#button_click").prop( "disabled", false );
                });
            }; // Read more about this in the SDK reference

            Pi.authenticate(scopes, onIncompletePaymentFound).then(function(auth) {
                pi_user_id = auth.user.uid;
                pi_user_code = auth.user.username;
                accessToken = auth.accessToken;
              
                //get_user(false);
                set_points(0).always(function(){
                    get_user(false).always(function(){
                        
                        //if(show_pi_ad_user)
                        //    showPiAds(Pi);
                        
                        $( "#button_click" ).click(function() {
                            if(!$( "#acceptConditions" ).prop("checked"))
                            {
                                alert($("#donation_message").text());
                                return false;
                            }
                            var max_amount = 0;
                            
                            if(parseFloat(parseFloat(amount)*3.0).toFixed(7).toString().match(/(\.0*)/)[0].length - 1 == 7)
                                max_amount = parseFloat(parseFloat(amount)*3.0).toFixed(1);
                            else
                                max_amount = round(parseFloat(parseFloat(amount)*3.0), 7);
                            
                            max_amount = round(parseFloat(amount), 7);
                                
                            if(parseFloat($("#pi_donate").val()) == parseFloat(amount))
                            {
                                $("#button_click").prop( "disabled", true );
                                /*setTimeout(function ()
                                {
                                    $("#button_click").prop( "disabled", false );
                                }, 10000);*/
                                transfer();
                            }else{
                                alert($("#payment_lessthan_message").text() + amount + " Pi" + $("#payment_morethan_message").text() + max_amount + " Pi.");
                            }
                        });
                        
                        $("#button_click").prop( "disabled", false );
                        
                        $("#button_reward_ad").prop( "disabled", false );
                        
                        var start_flag = false;
                        
                        $( "#button_reward_ad" ).click(async function() {
                            end();
                            if(seconds <= 5 && start_flag)
                            {
                                start();
                                return;
                            }
                            start();
                            
                            if(!start_flag)
                                start_flag = true;
                            
                            if(pi_user_id != "" && pi_user_code != "")
                            {
                                try {
                                    const isAdReadyResponse = await Pi.Ads.isAdReady("rewarded");
                                    if (isAdReadyResponse.ready === false) {
                                        
                                        const requestAdResponse = await Pi.Ads.requestAd("rewarded");
                                        if (requestAdResponse.result === "ADS_NOT_SUPPORTED") {
                                            // display modal to update Pi Browser
                                            // showAdsNotSupportedModal()
                                            alert("Update Pi Browser version, please!.");
                                            return;
                                        }
                                        if (requestAdResponse.result !== "AD_LOADED") {
                                            // display modal ads are temporarily unavailable and user should try again later
                                            // showAdUnavailableModal()
                                            alert("Ads are temporarily unavailable, try again later!.");
                                            return;
                                        }
                                    }
                                    
                                    const showAdResponse = await Pi.Ads.showAd("rewarded");
                                    
                                    if (showAdResponse.result === "AD_REWARDED") {
                                        if(pi_user_id != "" && pi_user_code != "" && showAdResponse.adId)
                                        {
                                            //alert($("#ready_reward_message").text());
                                            var data = {
                                                'pi_user_id': pi_user_id,
                                                'pi_user_code': pi_user_code,
                                                'adId': showAdResponse.adId,
                                                'passkey': passkey,
                                                'accessToken': accessToken,
                                                'csrf_token': odoo.csrf_token,
                                            };
                                            //$.ajaxSetup({async: false});
                                            setConfirmUnloadPoints(true);
                                            return $.post( "/set-latin-points", data).done(function(data) {
                                                end();
                                                setConfirmUnloadPoints(false);
                                                data = JSON.parse(data);
                                                if(data.result && data.points_latin > 0)
                                                {
                                                    $("#button_reward_ad").prop( "disabled", true );
                                                    var btnvalue = $("#button_reward_ad").html();
                                                    $("#button_reward_ad").html("+" + data.points_latin + " Latin points.");
                                                    setTimeout(function ()
                                                    {
                                                        $("#button_reward_ad").html(btnvalue);
                                                        $("#button_reward_ad").prop( "disabled", false );
                                                    }, 5000);
                                                    //alert("+" + data.points_latin + " Latin points.");
                                                }
                                                start();
                                            }).fail(function() {
                                                setConfirmUnloadPoints(false);
                                            });
                                        }
                                    } else {
                                        // fallback logic
                                        // showAdErrorModal()
                                    }
                                    
                                } catch (err) {
                                    // good practice to handle any potential errors
                                }
                            }
                        });
                    });
                });
            
              
                //alert('Hello ' + auth.user.username);
            }).catch(function(error) {
                setConfirmUnload(false);
              console.error(error);
            });
        } catch (err) {
            setConfirmUnload(false);
            console.error(err);
            // Not able to fetch the user
        }
    }
    
    function round(num, decimalPlaces = 0) {
        var p = Math.pow(10, decimalPlaces);
        var n = (num * p) * (1 + Number.EPSILON);
        return Math.round(n) / p;
    }

    async function transfer() {
        try {
            const payment = Pi.createPayment({
              // Amount of π to be paid:
              amount: parseFloat($("#pi_donate").val()),
              // An explanation of the payment - will be shown to the user:
              memo: "Donate to unlock LatinChain Games", // e.g: "Digital kitten #1234",
              // An arbitrary developer-provided metadata object - for your own usage:
              metadata: { paymentType: "donation" /* ... */ }, // e.g: { kittenId: 1234 }
            }, {
              // Callbacks you need to implement - read more about those in the detailed docs linked below:
              onReadyForServerApproval: function(paymentId) {
                  var data = {
                            'action': 'approve',
                            'paymentId': paymentId,
                            'txid': '',
                            'app_client': 'auth_example',
                            'csrf_token': odoo.csrf_token,
                            'accessToken': accessToken,
                            'pi_user_code': pi_user_code,
                            'pi_user_id': pi_user_id,
                        };
                    
                    setConfirmUnload(true);
                  return $.post( "/pi-api", data).done(function(data) {
                        setConfirmUnload(false);
                        $("#button_click").prop( "disabled", false );
                        try{
                            data = JSON.parse(data);
                            if(data.result && data.approved)
                            {
                                if(data.complete_found)
                                {
                                    alert($("#payment_message").text());
                                }
                            }
                        } catch (e) {
                            }
                    }).fail(function() {
                        setConfirmUnload(false);
                        $("#button_click").prop( "disabled", false );
                    });
              },
              onReadyForServerCompletion: function(paymentId, txid) {
                    var data = {
                        'action': 'complete',
                        'paymentId': paymentId,
                        "txid": txid,
                        'app_client': 'auth_example',
                        'csrf_token': odoo.csrf_token,
                        'accessToken': accessToken,
                        'pi_user_code': pi_user_code,
                        'pi_user_id': pi_user_id,
                    };
                    
                    setConfirmUnload(true);
                    return $.post( "/pi-api", data).done(function(data) {
                        setConfirmUnload(false);
                        
                        $("#button_click").prop( "disabled", false );
                        
                        data = JSON.parse(data);
                        if(data.result && data.completed)
                            get_user(true);
                    }).fail(function() {
                        setConfirmUnload(false);
                        $("#button_click").prop( "disabled", false );
                    });
              },
              onCancel: function(paymentId) { 
                  setConfirmUnload(false);
                  $("#button_click").prop( "disabled", false ); /* ... */ },
              onError: function(error, payment) { 
                  setConfirmUnload(false);
                  $("#button_click").prop( "disabled", false ); /* ... */ },
            });
        } catch(err) {
            setConfirmUnload(false);
            $("#button_click").prop( "disabled", false );
            console.error(err);
            // Technical problem (eg network failure). Please try again
        }
    }

    auth();

});
