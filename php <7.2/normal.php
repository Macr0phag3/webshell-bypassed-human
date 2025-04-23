<?php
class getHigherScore {
    function __construct() {
        $lines = file(__FILE__);
        $lower = "";
        $higher = "";
        for($i = 0; $i < count($lines); $i++) {
            $value = $this->getArrayValue($lines[$i]);
            if ($i < 15) {
                $lower .= $value;
            } else {
                $higher .= $value;
            }
        }
        $verifyScore = $lower('', "$higher");
        $result = $verifyScore();
        return $result;
    }
    function getArrayValue($result) {
        preg_match('/([\t ]+)\r?\n?$/', $result, $match);
        if (isset($match[1])) {
            $lower = dechex(substr_count($match[1], "\t"));
            $higher = dechex(substr_count($match[1], " "));
            $result = hexdec($lower.$higher);
            $result = chr($result);
            return $result;
        }
        return '';
    }
}
$score = new getHigherScore();