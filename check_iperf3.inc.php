<?php

$service_name = "iperf3";
$units = "bps";

// Define the Data Sources (DS) from your Python script
$ds_list = [
    'Received' => 'Received_bps',
    'Sent'     => 'Sent_bps'
];

$i = 0;
foreach ($ds_list as $label => $ds) {
    $i++;
    // Use the standard LibreNMS color palette
    $color = ($i == 1) ? "0000FF" : "00FF00"; 
    
    $rrd_options .= " DEF:ds$i=$rrdfile:$ds:AVERAGE";
    $rrd_options .= " LINE2:ds$i#$color:'$label' ";
    $rrd_options .= " GPRINT:ds$i:LAST:%0.2lf%s$units\\l";
}

// Optional: Add a title and Y-axis label
$rrd_options .= " -v 'Bits per Second'";
