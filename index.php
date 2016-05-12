<html>
    <head>
        <title>BootDev Tuning Panel</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <!--[if lte IE 8]><script src="assets/js/html5shiv.js"></script><![endif]-->
        <link rel="stylesheet" href="assets/css/main.css" />
        <!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
        <!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
        <noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
    </head>
    <body class="is-loading">
        <!--
        <script src="assets/js/ZeroClipboard.js"></script>
        <script src="assets/js/main.js"></script>
        <script src="assets/js/copy.js"></script>
        <script type="text/javascript" src="assets/js/jquery.min.js"></script>
        -->
        <script src="assets/js/clipboard.js"></script>
        <script src="assets/js/touche.js"></script>
	<!-- Wrapper -->
        <div id="wrapper">
            <!-- Main -->
            <section id="main">
                <header>
                    <img src="images/bootdev.png" width="200px">
                    <!--<h1>BootDev</h1>--><h1>Tuning&nbsp;Console</h1>
                    <p>Please input your server details for Tuning</p>
                </header>

<?php
require_once 'tools/functions.php';
$msg = '';
// Prepare variables.
// Run ec2-metadata to get instances information
/*
$instanceID = explode(" ",shell_exec('tools/ec2-metadata -i'))[1];
$instanceID = preg_replace('/\s+/', '', $instanceID);
$elasticIP = explode(" ",shell_exec('tools/ec2-metadata -v'))[1];
$elasticIP = preg_replace('/\s+/', '', $elasticIP);

// Get required information from system
$vpc_id = file_get_contents('data/vpc.txt');
$aws_credentials = file_get_contents('data/config');
$handle = fopen("data/config", "r");
$i = 0;
$aws_credentials = array();
$k = $v = '';
if ($handle) {
    while (($line = fgets($handle)) !== false) {
        // process the line read.
        $read = preg_replace('/\s+/', '', $line);
        if (strpos($read, '=') !== false)list($k, $v) = explode('=', $read);
        $aws_credentials[$k] = $v;
        $i++;
    }
    fclose($handle);
}
*/

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Show ICON
// Check if action is set
/*
if(!empty($_REQUEST['action'])){
    $action_set = true;
}

if(isset($action_set) && $action_set){
    if($_REQUEST['action'] == 'refresh'){
        include 'refresh.php';
    }
}
*/

if(!empty($_REQUEST['action'])){
    write_log('Action', $_REQUEST);
    $action_set = true;
}

if(isset($action_set) && $action_set){
write_log('POSTED_data',$_POST);
    if($_REQUEST['action'] == 'run'){
        //include 'refresh.php';
        if (count($_POST) > 0 && isset($_POST['hostname']) && isset($_POST['username'])){
            write_log('Post_exists', $_POST);
            if(!empty($_POST['password']) && !empty($_POST['key'])){
                write_log('Command_Check', 'Both Key and password exists');
                $msg = "Please provide only one between password and key";
            } elseif (!empty($_POST['password'])) {
                write_log('Command_Check', 'Using password to run');
                $command = 'python ./python/check.py -h ' . $_POST['hostname'] . ' -u ' . $_POST['username'] . ' -p ' . $_POST['password'];
                $response = shell_exec($command);
                write_log('Python_response', $response);
                write_log("Pythong_command", $command);
            } elseif (!empty($_POST['key'])) {
                write_log('Command_Check', 'Using Key to run');
                $key = fopen("key.pem", "w");
                fwrite($key, $_POST['key']);
                fclose($key);
            }
        } else {
            $msg = "Please input hostname and username";
        }
    }
}
?>
<!--
<form class="form-no-horizontal-spacing" id="refreshForm" action="index.php?action=refresh" method="post">
    <button class="btn btn-primary btn-cons" type="submit" ><p>IP </p><img src="images/refresh.png" alt="Change IP" style="max-width:100%;max-height:100%;height:80%;vertical-align:middle;position: relative;top: -3px;" /></button>
</form>

<form class="form-no-horizontal-spacing" id="reloadForm" action="index.php" method="post">
    <button class="btn btn-primary btn-cons" type="submit" ><p>Check </p><img src="images/check.png" alt="Check Current IP" style="max-width:100%;max-height:100%;height:80%;vertical-align:middle;position: relative;top: -3px;" /></button>
</form>
-->
<form class="form-no-horizontal-spacing" id="tune" action="index.php?action=run" method="post">
    <div align="right">
        <h6 style='display:inline;'>Hostname or IP</h6>
        <input style='display:inline;' name="hostname" type="textarea" placeholder="192.168.0.1"/>
    </div>
    <div align="right">
        <h6 style='display:inline;'>Username to login</h6>
        <input style='display:inline;' name="username" type="textarea" placeholder="root"/>
    </div>
    <div align="right">
        <h5 style='display:inline;' color="red" class="warning">*</h5>
        <h6 style='display:inline;'>Password</h6>
        <input style='display:inline;' name="password" type="textarea" placeholder="******"/>
    </div>
    <div align="right">
        <h5 style='display:inline;' color="red" class="warning">*</h5>
        <h6 style='display:inline;'>ssh key content</h6>
        <input name="key" type="textarea" rows="10" cols="50" />
    </div>
    <div color="red" >* input either one</div>
    <p>
        <button class="btn btn-primary btn-cons" type="submit" ><p>Tune! </p><img src="images/check.png" alt="Run tuning" style="max-width:100%;max-height:100%;height:80%;vertical-align:middle;position: relative;top: -3px;" /></button>
    </p>
</form>

<?php
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Show INFO
//echo "Instance ID = " . $instanceID . '<br>';
?>
<!--
                         <b>Current IP: </b>
-->
                         <!--
                         <button id="target-to-copy" data-clipboard-target="clipboard-text">
                         -->
<!--
                         <input type="text" id="copyTarget" value="<?php echo $elasticIP; ?>">
                         <button id="copyButton">Copy</button>
-->
<!--
                         <p name="clipboard-text" id="clipboard-text" class="clipboard-text">
<?php 
//    echo $elasticIP; 
?>
                         </p>
-->
                         <!--
                         <img src="images/copy.png" alt="Click to copy" style="max-width:100%;max-height:100%;height:80%;vertical-align:middle;position: relative;top: -3px;" />
                         -->
                         <!--
                         </button>
                         -->
<!--
<textarea id="txt"><?php //echo $elasticIP; ?></textarea>
<div align="center"><button class="btn-md" onclick="copy();">copy</button></div>
-->
<!--<button id='markup-copy'>Copy Button</button>-->
<!--<textarea id="txt"><?php // echo $elasticIP; ?></textarea>-->
<!--<p><i>Copy only works in Desktop Browser</i><p>-->
<script>
    var my_var = "<?php // echo $elasticIP; ?>";
function addMultipleListeners(element,events,handler,useCapture,args){
  if (!(events instanceof Array)){
    throw 'addMultipleListeners: '+
          'please supply an array of eventstrings '+
          '(like ["click","mouseover"])';
  }
  //create a wrapper for to be able to use additional arguments
  var handlerFn = function(e){
    handler.apply(this, args && args instanceof Array ? args : []);
  }
  for (var i=0;i<events.length;i+=1){
    element.addEventListener(events[i],handlerFn,useCapture);
  }
}

function handler(e) {
  // do things
        clipboard.copy({
            'text/plain': my_var,
            'text/html': '<i>here</i> is some <b>rich text</b>'
        }).then(
            function(){console.log('success'); },
            function(err){console.log('failure', err);
        });
};

// usage
addMultipleListeners(document.getElementById('markup-copy'),
                     ['touchstart','click'],handler,false);
</script>
<?php
//echo "VPC = " . $vpc_id . '<br>';
//echo "aws_access_key_id = " . $aws_credentials['aws_access_key_id'] . '<br>';
//echo "aws_secret_access_key = " . $aws_credentials['aws_secret_access_key'] . '<br>';
//echo "region = " . $aws_credentials['region'] . '<br>';
?>
                </section>
                <!-- Footer -->
                <footer id="footer">
<?php
/*
$README = fopen('README.md', 'r');
$line = fgets($README);
fclose($f);
echo 'console version v' . explode("=",$line)[1];
*/
?>
                <ul class="copyright">
                    <li>&copy; BootDev</li>
                    <li>Tuning Demo</li>
                </ul>
            </footer>
        </div>
        <!-- Scripts -->
        <!--[if lte IE 8]><script src="assets/js/respond.min.js"></script><![endif]-->
        <script>
            if ('addEventListener' in window) {
                window.addEventListener('load', function() { document.body.className = document.body.className.replace(/\bis-loading\b/, ''); });
                document.body.className += (navigator.userAgent.match(/(MSIE|rv:11\.0)/) ? ' is-ie' : '');
            }
        </script>
        <!--
        <script>
            var clientTarget = new ZeroClipboard( $("#target-to-copy"), {
                moviePath: "assets/js/ZeroClipboard.swf",
                debug: false
            } );

            clientTarget.on( "load", function(clientTarget){
                $('#flash-loaded').fadeIn();
                clientTarget.on( "complete", function(clientTarget, args) {
                    clientTarget.setText( args.text );
                    $('#target-to-copy-text').fadeIn();
                } );
            } );
        </script>
        -->
    <script>
        function copy()
        {
            try
            {
                $('#txt').select();
                document.execCommand('copy');
            }
            catch(e)
            {
                alert(e);
            }
        }
    </script>
    </body>
</html>
