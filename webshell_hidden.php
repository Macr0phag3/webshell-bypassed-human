<?php						   
class getHigherScore {						 
    function __construct() {						            
        $lines = file(__FILE__);						            
        $lower = "";					               
        $higher = "";							     
        $top = "";							   
        for($i = 0; $i < count($lines); $i++) {						     
            $value = $this->getArrayValue($lines[$i]);							  
            if ($i < 14) {					               
                $lower .= $value;						      
            } else if ($i < 20) {							     
                $higher .= $value;						              
            } else {						   
                $top .= $value;							   
            }							         
        }							   
        $result = $lower("$higher", $top);							    
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
						  
							         
		
					    
							  
			
							         
		
			          
		         
		  
