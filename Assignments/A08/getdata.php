<?php

for($i = 0;$i<100;$i++){
    $data = file_get_contents("https://my.api.mockaroo.com/tdata.json?key=46f2deb0");
    if($i<10){
        $name = "000{$i}";
    }elseif($i<100){
        $name = "00{$i}";
    }elseif($i<1000){
        $name = "0{$i}";
    }
    file_put_contents("./data/{$name}.json",$data);
    sleep(1);
}