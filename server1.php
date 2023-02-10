<?php

    /*$file = fopen("./server.log", "a");
    fwrite($file , "\nAccessed " . date("Y-m-d H:i:s") . "\n");
    fwrite($file , "\n_POST " . print_r($_POST, true) . "\n");
    fclose($file );*/

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
    $apps['auth_app1'] = 'Key <your Server API Key>';
    $apps['auth_app2'] = 'Key <your Server API Key>';
    $apps['auth_app3'] = 'Key <your Server API Key>';
    $apps['auth_app4'] = 'Key <your Server API Key>';
    
    $ch = curl_init($url);
    # Form data string
    $postString = http_build_query($data, '', '&');
    # Setting our options
    $headers = array(
       "Authorization: Key " . $apps[$_POST['app_client']],
    );
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    # Get the response
    $response = curl_exec($ch);
    $error = curl_error($ch);
    curl_close($ch);
    
    /*$file = fopen("./server.log", "a");
    fwrite($file , "\nResponse " . date("Y-m-d H:i:s") . "\n");
    fwrite($file , $response);
    fwrite($file , "\nError\n");
    fwrite($file , $error);
    fwrite($file , "\n");
    fclose($file );*/

    //var_dump($response);
    header("HTTP/1.1 200 OK");
    header('Content-Type: application/json');
    echo json_encode($response);
?>
