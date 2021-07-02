<?php

    if($_POST['action'] == "approve")
    {
        $url = 'https://api.minepi.com/v2/payments/'.$_POST['paymentId'].'/approve';
        $data = array();
    }else if($_POST['action'] == "complete")
    {
        $url = 'https://api.minepi.com/v2/payments/'.$_POST['paymentId'].'/complete';
        $data = array('txid' => $_POST['txid']);
    }
    
    $apps = array();
    $apps['auth_pidoku'] = 'Key <your Server API Key>';
    $apps['auth_snake'] = 'Key <your Server API Key>';
    $apps['auth_example'] = 'Key <your Server API Key>';
    
    $ch = curl_init($url);
    # Form data string
    $postString = http_build_query($data, '', '&');
    # Setting our options
    $headers = array(
       "Authorization: " . $apps[$_POST['app_client']],
    );
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    # Get the response
    $response = curl_exec($ch);
    curl_close($ch);

    //var_dump($response);
    header("HTTP/1.1 200 OK");
    header('Content-Type: application/json');
    echo json_encode($response);
    
    /*$file = fopen("./file.txt", "a");
    fwrite($file , json_encode($response));
    fclose($file );*/
?>
