const fs = require('fs');

getRequest = (file) => {

    const lineReader = require('line-reader');

    lineReader.eachLine(`${file}/${file}.txt`, function(line, last) {

        /* Find HTTP request */
        if (line.indexOf('GET') !== -1 || line.indexOf('POST') !== -1) {

            /* Request needs to be SQL-related */
            if (line.indexOf('=') !== -1) {

                if (file === "anomalousTrafficTest") {
                    if (line.toLowerCase().indexOf('where') !== -1 || line.toLowerCase().indexOf('select') !== -1 || line.toLowerCase().indexOf('drop') !== -1) {
                        fs.appendFile(`${file}/requests.txt`, line + '\n', function (err) {
                            if (err) throw err;
                        });
                    }
                }
                else {
                    fs.appendFile(`${file}/requests.txt`, line + '\n', function (err) {
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

// getRequest('normalTrafficTest');
getRequest('anomalousTrafficTest');