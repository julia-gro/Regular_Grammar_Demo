grammar regSumFormula ;

gb          : [A-Z] gb | [a-z] kb | [0-9] ziffer | $ ;
kb          : [A-Z] gb | [0-9] ziffer  | $ ;
ziffer      : [A-Z] gb | [0-9] ziffer  | $ ;
$           : EOF ;


