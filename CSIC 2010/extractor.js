const fs = require('fs');
const t = require('./encoding');


getRequest = (file) => {

    const lineReader = require('line-reader');
    lineReader.eachLine(`${file}/${file}.txt`, function(line, last) {
        /* Find HTTP request */
        if (line.indexOf('GET') !== -1 || line.indexOf('POST') !== -1) {

            line = line.split(' ')[1];
            const uri_dec = decodeURIComponent(escape(line));
            /* Request needs to be SQL-related */
            if (uri_dec.indexOf('=') !== -1) {

                if (file === "anomalousTrafficTest") {
                    if (uri_dec.toLowerCase().indexOf('where') !== -1 || uri_dec.toLowerCase().indexOf('select') !== -1 || uri_dec.toLowerCase().indexOf('drop') !== -1) {
                        fs.appendFileSync(`${file}/requests.txt`, uri_dec + '\n', function (err) {
                            if (err) throw err;
                        });
                    }
                }
                else {
                    fs.appendFileSync(`${file}/requests.txt`, uri_dec + '\n', function (err) {
                        if (err) throw err;
                    });
                }

            }
        }
        if (last) {
            console.log('Done');
        }
    });

}

tokenize = (file) => {
    const lineReader = require('line-reader');

    lineReader.eachLine(`${file}/requests.txt`, function(line, last) {

        /* Find queries */
        if (line.indexOf('?') !== -1) {

            /* Find first query */
            const index = line.indexOf('?');
            let queryOnly = line.substring(index + 1, line.length);
            let paramIndex;

            /* Write token */
            let onlyOneToken = true;
            while ((paramIndex = queryOnly.indexOf('&')) !== -1) {
                onlyOneToken = false;
                /* Save each x=y token */
                const newParam = queryOnly.substring(0, paramIndex);
                queryOnly = queryOnly.substring(paramIndex + 1, queryOnly.length);
                fs.appendFileSync(`${file}/tokens.txt`, newParam + ' ' , function (err) {
                    if (err) throw err;
                });
            }
            if (onlyOneToken) {
                fs.appendFileSync(`${file}/tokens.txt`, queryOnly + ' ' , function (err) {
                    if (err) throw err;
                });
            }
            fs.appendFileSync(`${file}/tokens.txt`, '\n' , function (err) {
                if (err) throw err;
            });
        }
        if (last) {
            console.log('Done');
        }
    });
}

// translate = (file) => {
//     const lineReader = require('line-reader');

//     lineReader.eachLine(`${file}/tokens.txt`, function(line, last) {

//         /* Find queries */
//         for (var item of t.codes) {
//             // var regex = new RegExp(item, "g");
            
//             line = decodeURIComponent(line);
//         }
//         fs.appendFileSync(`${file}/translatedTokens.txt`, line + '\n' , function (err) {
//             if (err) throw err;
//         });
//         if (last) {
//             console.log('Done');
//         }
//     });
// }

getRequest('normalTrafficTest');
getRequest('anomalousTrafficTest');

// tokenize('normalTrafficTest');
// tokenize('anomalousTrafficTest');

// translate('normalTrafficTest');
// translate('anomalousTrafficTest');