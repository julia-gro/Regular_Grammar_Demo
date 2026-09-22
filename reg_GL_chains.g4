grammar reg_GL_chains;

mg_chain_1                  : [0-9] mg_digit_1a | 'O-' mg_ether_1 | 'P-' mg_ether_1;
mg_digit_1a                 : [0-9] mg_digit_1a | ':' mg_colon_1;
mg_colon_1                  : [0-9] mg_digit_1b;
mg_digit_1b                 : [0-9] mg_digit_1b | '/' mg_chain_2 | ';' mg_semicolon_1b | $;
mg_chain_2                  : [0-9] mg_digit_2a | 'O-' mg_ether_2 | 'P-' mg_ether_2;
mg_digit_2a                 : [0-9] mg_digit_2a | ':' mg_colon_2;
mg_colon_2                  : [0-9] mg_digit_2b;
mg_digit_2b                 : [0-9] mg_digit_2b | '/' mg_chain_3;
mg_chain_3                  : [0-9] mg_digit_3a | 'O-' mg_ether_3 | 'P-' mg_ether_3;
mg_digit_3a                 : [0-9] mg_digit_3a | ':' mg_colon_3;
mg_colon_3                  : [0-9] mg_digit_3b;
mg_digit_3b                 : [0-9] mg_digit_3b | ';' mg_semicolon_3b | $;

dg_chain_1                  : [0-9] dg_digit_1a | 'O-' dg_ether_1 | 'P-' dg_ether_1;
dg_digit_1a                 : [0-9] dg_digit_1a | ':' dg_colon_1;
dg_colon_1                  : [0-9] dg_digit_1b;
dg_digit_1b                 : [0-9] dg_digit_1b | '/' dg_chain_2 | '_' dg_underscore_chain_2 | ';' dg_semicolon_1b | $;
dg_chain_2                  : [0-9] dg_digit_2a | 'O-' dg_ether_2 | 'P-' dg_ether_2;
dg_digit_2a                 : [0-9] dg_digit_2a | ':' dg_colon_2;
dg_colon_2                  : [0-9] dg_digit_2b;
dg_digit_2b                 : [0-9] dg_digit_2b | '/' dg_chain_3;
dg_chain_3                  : [0-9] dg_digit_3a | 'O-' dg_ether_3 | 'P-' dg_ether_3;
dg_digit_3a                 : [0-9] dg_digit_3a | ':' dg_colon_3;
dg_colon_3                  : [0-9] dg_digit_3b;
dg_digit_3b                 : [0-9] dg_digit_3b | ';' dg_semicolon_3b | $;
dg_underscore_chain_2             : [0-9] dg_underscore_digit_2a | 'O-' dg_underscore_ether_2 | 'P-' dg_underscore_ether_2;
dg_underscore_digit_2a            : [0-9] dg_underscore_digit_2a | ':' dg_underscore_colon_2;
dg_underscore_colon_2             : [0-9] dg_underscore_digit_2b;
dg_underscore_digit_2b            : [0-9] dg_underscore_digit_2b | ';' dg_underscore_semicolon_2b | $;

tg_chain_1                  : [0-9] tg_digit_1a | 'O-' tg_ether_1 | 'P-' tg_ether_1;
tg_digit_1a                 : [0-9] tg_digit_1a | ':' tg_colon_1;
tg_colon_1                  : [0-9] tg_digit_1b;
tg_digit_1b                 : [0-9] tg_digit_1b | '/' tg_chain_2 | '_' tg_underscore_chain_2 | ';' tg_semicolon_1b | $;
tg_chain_2                  : [0-9] tg_digit_2a | 'O-' tg_ether_2 | 'P-' tg_ether_2;
tg_digit_2a                 : [0-9] tg_digit_2a | ':' tg_colon_2;
tg_colon_2                  : [0-9] tg_digit_2b;
tg_digit_2b                 : [0-9] tg_digit_2b | '/' tg_chain_3;
tg_chain_3                  : [0-9] tg_digit_3a | 'O-' tg_ether_3 | 'P-' tg_ether_3;
tg_digit_3a                 : [0-9] tg_digit_3a | ':' tg_colon_3;
tg_colon_3                  : [0-9] tg_digit_3b;
tg_digit_3b                 : [0-9] tg_digit_3b | ';' tg_semicolon_3b | $;
tg_underscore_chain_2             : [0-9] tg_underscore_digit_2a | 'O-' tg_underscore_ether_2 | 'P-' tg_underscore_ether_2;
tg_underscore_digit_2a            : [0-9] tg_underscore_digit_2a | ':' tg_underscore_colon_2;
tg_underscore_colon_2             : [0-9] tg_underscore_digit_2b;
tg_underscore_digit_2b            : [0-9] tg_underscore_digit_2b | '_' tg_underscore_chain_3;
tg_underscore_chain_3             : [0-9] tg_underscore_digit_3a | 'O-' tg_underscore_ether_3 | 'P-' tg_underscore_ether_3;
tg_underscore_digit_3a            : [0-9] tg_underscore_digit_3a | ':' tg_underscore_colon_3;
tg_underscore_colon_3             : [0-9] tg_underscore_digit_3b;
tg_underscore_digit_3b            : [0-9] tg_underscore_digit_3b | ';' tg_underscore_semicolon_3b | $;



// One ';O...' trailer per chain, so a chain carrying an oxygen count can
// still be followed by the next chain. Sharing a single trailer could not:
// it had no way to know which chain to return to. Same shape as reg_SP_chains.g4.
mg_semicolon_1b                   : 'O' mg_oxygen_1b;
mg_oxygen_1b                      : [0-9] mg_oxygen_count_1b | '/' mg_chain_2 | $;
mg_oxygen_count_1b                : [0-9] mg_oxygen_count_1b | '/' mg_chain_2 | $;
mg_semicolon_3b                   : 'O' mg_oxygen_3b;
mg_oxygen_3b                      : [0-9] mg_oxygen_count_3b | $;
mg_oxygen_count_3b                : [0-9] mg_oxygen_count_3b | $;
dg_semicolon_1b                   : 'O' dg_oxygen_1b;
dg_oxygen_1b                      : [0-9] dg_oxygen_count_1b | '/' dg_chain_2 | '_' dg_underscore_chain_2 | $;
dg_oxygen_count_1b                : [0-9] dg_oxygen_count_1b | '/' dg_chain_2 | '_' dg_underscore_chain_2 | $;
dg_semicolon_3b                   : 'O' dg_oxygen_3b;
dg_oxygen_3b                      : [0-9] dg_oxygen_count_3b | $;
dg_oxygen_count_3b                : [0-9] dg_oxygen_count_3b | $;
dg_underscore_semicolon_2b        : 'O' dg_underscore_oxygen_2b;
dg_underscore_oxygen_2b           : [0-9] dg_underscore_oxygen_count_2b | $;
dg_underscore_oxygen_count_2b     : [0-9] dg_underscore_oxygen_count_2b | $;
tg_semicolon_1b                   : 'O' tg_oxygen_1b;
tg_oxygen_1b                      : [0-9] tg_oxygen_count_1b | '/' tg_chain_2 | '_' tg_underscore_chain_2 | $;
tg_oxygen_count_1b                : [0-9] tg_oxygen_count_1b | '/' tg_chain_2 | '_' tg_underscore_chain_2 | $;
tg_semicolon_3b                   : 'O' tg_oxygen_3b;
tg_oxygen_3b                      : [0-9] tg_oxygen_count_3b | $;
tg_oxygen_count_3b                : [0-9] tg_oxygen_count_3b | $;
tg_underscore_semicolon_3b        : 'O' tg_underscore_oxygen_3b;
tg_underscore_oxygen_3b           : [0-9] tg_underscore_oxygen_count_3b | $;
tg_underscore_oxygen_count_3b     : [0-9] tg_underscore_oxygen_count_3b | $;




// ether / plasmanyl-plasmenyl chain prefixes: 'O-16:0', 'P-16:0'.
// Each one only consumes the prefix and hands the digits back to the
// chain's own digit state, so chain shapes stay untouched.
mg_ether_1                        : [0-9] mg_digit_1a;
mg_ether_2                        : [0-9] mg_digit_2a;
mg_ether_3                        : [0-9] mg_digit_3a;
dg_ether_1                        : [0-9] dg_digit_1a;
dg_ether_2                        : [0-9] dg_digit_2a;
dg_ether_3                        : [0-9] dg_digit_3a;
dg_underscore_ether_2             : [0-9] dg_underscore_digit_2a;
tg_ether_1                        : [0-9] tg_digit_1a;
tg_ether_2                        : [0-9] tg_digit_2a;
tg_ether_3                        : [0-9] tg_digit_3a;
tg_underscore_ether_2             : [0-9] tg_underscore_digit_2a;
tg_underscore_ether_3             : [0-9] tg_underscore_digit_3a;

$                           : EOF;


// Basic Lexer Tokens
WHITESPACE                  : [ \t]+ -> skip ;
NEWLINE                     : [\r\n]+ -> skip ;
