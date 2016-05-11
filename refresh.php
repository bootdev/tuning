<?php
// Require the PHP SDK of AWS
require 'vendor/autoload.php';
use Aws\Ec2\Ec2Client;

// Begin EC2Client
$ec2 = Ec2Client::factory(array(
  'region'  => $aws_credentials['region'],
  'version' => 'latest',
  'credentials' => array(
    'key'    => $aws_credentials['aws_access_key_id'],
    'secret' => $aws_credentials['aws_secret_access_key'],
  )
));

// Test if Ec2Client is working
/*
$result = $ec2->describeInstanceStatus([
  'IncludeAllInstances' => true,
  'InstanceIds' => [ $instanceID ],
]);
*/

// Get new address
$allocation = $ec2->allocateAddress([
    'Domain' => $vpc_id,
]);
$allocation = reset($allocation);

// Disassociate if the instance is attached with EIP
$get_ip = true;
try {
	$describeEIP = $ec2->describeAddresses([
            'PublicIps' => [ $elasticIP ],
        ]);
        $describeEIP = reset($describeEIP);
} catch (Exception $e) {
    $get_ip = false;
}

// IF EIP is attached, run disassociate.
if($get_ip){
    $result = $ec2->disassociateAddress([
        //'AssociationId' => $describeEIP['Addresses'][0]['AssociationId'],
        'PublicIp' => $elasticIP,
    ]);
} 

// Assoicate new EIP
$result = $ec2->associateAddress([
    'AllocationId' => $allocation["AllocationId"],
    'InstanceId' => $instanceID,
//    'PublicIp' => $allocation["PublicIp"],
]);

// Release EIP
if($get_ip){
    $result = $ec2->releaseAddress([
        'AllocationId' => $describeEIP['Addresses'][0]['AllocationId'],
        //'PublicIp' => $elasticIP,
    ]);
}
echo '<br>';
echo 'New IP = ' . $allocation["PublicIp"];
