const fs = require('fs');

getRequest = (file) => {

    const lineReader = require('line-reader');

    lineReader.eachLine(`${file}/${file}.txt`, function(line, last) {

        /* Find HTTP request */
        if (line.indexOf('GET') !== -1 || line.indexOf('POST') !== -1) {
            /* Request needs to have related */
            fs.appendFile(`${file}/requests.txt`, line + '\n', function (err) {
                if (err) throw err;
            });
        }
        if (last) {
            console.log('Done');
        }
    });
      
}

getRequest('normalTrafficTest');