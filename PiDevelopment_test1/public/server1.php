<?php

    if($_GET['action'] == "approve")
    {
        $url = 'https://api.minepi.com/v2/payments/'.$_GET['paymentId'].'/approve';
        $data = array();
    }else if($_GET['action'] == "complete")
    {
        $url = 'https://api.minepi.com/v2/payments/'.$_GET['paymentId'].'/complete';
        $data = array('txid' => $_GET['txid']);
    }
    
    $apps = array();
    $apps['auth_pidoku'] = 'Key f6abrmg3e67qxpp8g4mdkteefsxsejsid84jjavkwvhpjcdylmc9wqbpvgbab9vv';
    $apps['auth_snake'] = 'Key xymiz9lfmdhmtktkpfhl0yxjwhnsz7gdbmcie4obtbvpydgrh911qn1hwuhmhqgn';
    $apps['auth_example'] = 'Key 0frba6nmg2dgeyunmlziyzsxkagymb4y0ezjmuufti2pooi15b7mciq78707of4q';
    
    $ch = curl_init($url);
    # Form data string
    $postString = http_build_query($data, '', '&');
    # Setting our options
    $headers = array(
       "Authorization: " . $apps[$_GET['app_client']],
       "Accept: application/json",
       "Content-Type: application/json",
    );
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    # Get the response
    $response = curl_exec($ch);
    curl_close($ch);

    var_dump($response);
?>
