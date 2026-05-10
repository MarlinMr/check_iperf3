<?php
$service_name = "iperf3";

$ds_list = [
    'Received' => 'Received_bps',
    'Sent'     => 'Sent_bps',
    'Retries'  => 'Retries',
    'Jitter'   => 'Jitter_ms',
    'Loss'     => 'Loss_Percent'
];

$colors = ["0000FF", "00FF00", "FF0000", "FF00FF", "00FFFF"];
$i = 0;

foreach ($ds_list as $label => $ds) {
    $i++;
    $color = $colors[$i-1];
    $rrd_options .= " DEF:ds$i=$rrdfile:$ds:AVERAGE";
    $rrd_options .= " LINE2:ds$i#$color:'$label' ";
    $rrd_options .= " GPRINT:ds$i:LAST:%0.2lf%s\\l";
}

$rrd_options .= " -v 'iperf3 Metrics'";
