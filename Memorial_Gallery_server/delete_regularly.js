//
// Execute as a root ($ sudo node delete_regularly.js)
//

const moment = require('moment')

const mysql = require('mysql')
const sql_con = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: process.env.password,
    database: 'star_gallery',
    timezone: 'jst',
    insecureAuth : true
})

sql_con.connect(function(err){
    if(err){
        console.log("\nUsage:\n\t$ password='' node " + process.argv[1].replace(/^.*[\\\/]/, ''))
        process.exit(1)
    }
    console.log("[*] MySql, OK")
})

const now = moment().format('YYYYMMDD')
sql_con.query('SELECT filename FROM photos WHERE expire < ?', [now], function(err, rows, fields) {
    if (err) throw err
    const { spawn } = require('child_process');
    
    rows.forEach(function(row){
        console.log("[*] Filename : " + row.filename)
        const child = spawn('rm', ['/usr/share/nginx/node/composed_images/'+row.filename]);
        child.stdout.on('data', function(data) {
            console.log(data.toString());
        });
    })
})

sql_con.query('DELETE FROM photos WHERE expire < ?', [now], function(err, rows, fields) {
    if (err) throw err

    console.log("[*] DELETED where expire < " + now)
})

sql_con.end(function(err) {
    if (err) {
        console.log("Error Occured" + err.stack)
    }
    console.log('Disconnected to mysql');
});
