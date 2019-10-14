const codes = [
    '%27',
    '%3B',
    '%25',
    '%F3',
    '%E9',
    '%F1',
    '%2C',
    '%2F',
    '%3F',
    '%FC',
    '%40',
    '%24',
    '%E7',
    '%F6',
    '%E1',
    '%E0',
    '%ED',
    '%21',
    '%D1',
    '%FA',
    '%CD',
    '%2B'
]

const translate = (token) => {
    switch (token) {
        case '%27':
            return `'`;
        case '%3B':
            return ';'; 
        case '%25':
            return '%';
        case '%F3':
            return 'ó';  
        case '%E9':
            return 'é';
        case '%F1':
            return 'ñ';  
        case '%2C':
            return ',';
        case '%2F':
            return '/';  
        case '%3F':
            return '?';
        case '%FC':
            return 'ü';  
        case '%40':
            return '@';  
        case '%24':
            return '$'; 
        case '%E7':
            return 'ç';
        case '%F6':
            return 'ö'; 
        case '%E1':
            return 'á';
        case '%E0':
            return 'à';
        case '%ED':
            return 'í';
        case '%21':
            return '!';
        case '%D1':
            return 'Ñ';
        case '%2B':
            return '+';
        case '%FA':
            return 'ú';
        case '%CD':
            return 'Í';
        default:
            return '@@@@@@';
    }
}

module.exports = {
    codes: codes,
    translate: translate
}