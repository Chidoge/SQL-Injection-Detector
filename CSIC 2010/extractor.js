const fs = require('fs');

getRequest = (file) => {

    const lineReader = require('line-reader');

    lineReader.eachLine(`${file}/${file}.txt`, function(line, last) {

        /* Find HTTP request */
        if (line.indexOf('GET') !== -1 || line.indexOf('POST') !== -1) {

            line = line.split(' ')[1];
            /* Request needs to be SQL-related */
            if (line.indexOf('=') !== -1) {

                if (file === "anomalousTrafficTest") {
                    if (line.toLowerCase().indexOf('where') !== -1 || line.toLowerCase().indexOf('select') !== -1 || line.toLowerCase().indexOf('drop') !== -1) {
                        fs.appendFileSync(`${file}/requests.txt`, line + '\n', function (err) {
                            if (err) throw err;
                        });
                    }
                }
                else {
                    fs.appendFileSync(`${file}/requests.txt`, line + '\n', function (err) {
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

// getRequest('normalTrafficTest');
// getRequest('anomalousTrafficTest');

// tokenize('normalTrafficTest');
tokenize('anomalousTrafficTest');