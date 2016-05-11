<?php
// Log writing function
function write_log($str,$data_array) {
    date_default_timezone_set('UTC');
    $date=new DateTime();
    $textname = (string)$date->format('Ymd-H:i:s') . '_' . $str . ".txt"; //檔名  filename
    $URL = "log/";
    if(!is_dir($URL))                                 // 路徑中的$str 資料夾是否存在 Folder exists in the path
        mkdir($URL,0700);

    $URL .= $textname;                           //完整路徑與檔名 The full path and filename
    file_put_contents($URL, print_r($data_array, true));
}
