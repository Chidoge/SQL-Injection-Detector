const fs = require('fs');
const decode = require("urldecode")
const Moniker = require("moniker")

let varNames = Moniker.generator([Moniker.noun])

console.log(varNames.choose())
console.log(varNames.choose())
console.log(varNames.choose())

// Common SQL queries associate with POST, GET, UPDATE, DELETE
/*
    INSERT INTO table_name (column_1, column_2) VALUES (value_1, value_2);
    SELECT column_name FROM table_name WHERE condition;
    SELECT column_name FROM table_name;
    ALTER TABLE table_name SET column_1 = value_1 WHERE condition;
    DELETE FROM table_name WHERE condition;
*/

const SQLQueries = [
    "INSERT INTO table_name (VAR1, VAR2) VALUES (SQLI1, SQLI2) ",
    "SELECT column_name FROM table_name WHERE VAR1 = SQLI1 ",
    "ALTER TABLE table_name SET VAR1 = SQLI1 WHERE VAR2 = SQLI2 ",
    "DELETE FROM table_name WHERE VAR1 = SQLI1 "
]

/*
    Mode for creating data for:
    0: Normal Queries
    1: Malicious Queries
    2: Mix of normal and malicious querires
*/
let mode = 2;

console.log(SQLQueries[Math.floor(Math.random() * SQLQueries.length)])

const SQLIList = []

let normData;

fs.readFile("B:/Users/PJoe9/Desktop/CS760/query_generator/norm.txt", "utf8", (err, data) => {
    if (err) throw err;
    // Seperate SQLI queries
    normData = data.split(/\r?\n/)
    normData = normData.map(data => {
        if(decode(data) == -1) {
            return data
        } else {
            return decode(data)
        }
    })
})

fs.readFile("B:/Users/PJoe9/Desktop/CS760/query_generator/sqli.txt", "utf8", (err, data) => {
    if (err) throw err;
    // Seperate SQLI queries
    let sqliData = data.split(/\r?\n/)
    sqliData = sqliData.map(data => {
        if(decode(data) == -1) {
            return data
        } else {
            return decode(data)
        }
    })

    // Randomly generate 25000 queries
    for(i = 0; i < 25000; i++) {
        let genString = SQLQueries[Math.floor(Math.random() * SQLQueries.length)]
        // Generate Malicious Query
        if(mode == 0) {
            genString = genString.replace("table_name", varNames.choose())
            genString = genString.replace("column_name", varNames.choose())
            genString = genString.replace("VAR1", varNames.choose())
            genString = genString.replace("VAR2", varNames.choose())
            genString = genString.replace("SQLI1", normData[Math.floor(Math.random() * normData.length)])
            genString = genString.replace("SQLI2", normData[Math.floor(Math.random() * normData.length)])
            genString += "0 \n"
        } else if (mode == 1) {
            genString = genString.replace("table_name", varNames.choose())
            genString = genString.replace("column_name", varNames.choose())
            genString = genString.replace("VAR1", varNames.choose())
            genString = genString.replace("VAR2", varNames.choose())
            genString = genString.replace("SQLI1", sqliData[Math.floor(Math.random() * sqliData.length)])
            genString = genString.replace("SQLI2", sqliData[Math.floor(Math.random() * sqliData.length)])
            genString += "1 \n"
        } else if(mode == 2) {
            if(Math.floor(Math.random() * 2) == 1) {
                genString = genString.replace("table_name", varNames.choose())
                genString = genString.replace("column_name", varNames.choose())
                genString = genString.replace("VAR1", varNames.choose())
                genString = genString.replace("VAR2", varNames.choose())
                genString = genString.replace("SQLI1", sqliData[Math.floor(Math.random() * sqliData.length)])
                genString = genString.replace("SQLI2", sqliData[Math.floor(Math.random() * sqliData.length)])
                genString += "1 \n"
            } else {
                genString = genString.replace("table_name", varNames.choose())
                genString = genString.replace("column_name", varNames.choose())
                genString = genString.replace("VAR1", varNames.choose())
                genString = genString.replace("VAR2", varNames.choose())
                genString = genString.replace("SQLI1", normData[Math.floor(Math.random() * normData.length)])
                genString = genString.replace("SQLI2", normData[Math.floor(Math.random() * normData.length)])
                genString += "0 \n"
            }
        }
        console.log(`File was updated: ${i}`)

        try{
            fd = fs.openSync('mixTest.txt', 'a');
            fs.appendFileSync(fd, genString, 'utf8');
        } catch (err) {
            console.log(err)
        } finally {
            if (fd !== undefined)
            fs.closeSync(fd)
        }
    }
})