const bodyParser = require('body-parser')

// For Database(MySql)
const mysql = require('mysql')
const sql_con = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: process.env.password,
    database: 'star_gallery',
    insecureAuth : true,
    timezone: 'jst'
})
sql_con.connect(function(err){
    if(err){
        console.log("\nUsage:\n\t$ sudo password='' node " + process.argv[1].replace(/^.*[\\\/]/, ''))
        process.exit(1)
    }
    console.log("MySql Connected")
})

// For hash-function
const crypto = require('crypto')
function sha1hex(message){
    const sha1 = crypto.createHash('sha1')
    return sha1.update(message, 'binary').digest('hex')
}

function add_photo(filename, expire){
    sql_con.query("INSERT INTO photos (filename, expire) VALUES(?, ?)", [filename, expire], function(err, results, fields){
        if(err) throw err
        console.log("[*] Photo added")
    })
}

function image_compose(src_image, background_img, expire){
    const { PythonShell } = require('python-shell')
    PythonShell.run('./utils/compose.py', {args:[src_image, background_img]}, function(err, results){
        if(err) throw err
        console.log("[+] COMPOSE : " + results[0])
        add_photo(results[0], expire)
    })
}

const multer = require('multer')
const storage1 = multer.diskStorage({
    destination: './images',
    filename: function(req, file, cb){
        const file_hash = sha1hex(file.originalname)
        cb(null, file_hash + '.jpg')
    }
})
const uploader1 = multer({storage:storage1})
const express = require('express')
const app = express()

// POST 
app.post('/memorial', uploader1.single('image'), function(req, res){
    const file = req.file
    const file_hash = sha1hex(file.originalname)
    const expire = req.body.ExpirationDate
    const background_scene = req.body.SynthesusNumber

    console.log(file)
     
    // insert into Database
    image_compose('./images/'+file_hash+'.jpg', './background_images/'+background_scene+'.jpg', expire)
    //add_photo(filename, expire)

    res.status(200).json({msg: 'Uploaded'})
})

// GET composed images
app.get('/memorial/album', function(req, res){
    sql_con.query("SELECT * FROM photos", function(err, rows, fields) {
        if(err) throw err

        console.log(rows)
        res.render('index', {PhotoData: rows})
    })
})


const storage2 = multer.diskStorage({
    destination: './gallery',
    filename: function(req, file, cb){
        cb(null, file.originalname)
    }
})
const uploader2 = multer({storage:storage2})

// POST Gallery
app.post('/memorial/star-gallery', uploader2.single('image'), function(req, res){
    const file = req.file
    console.log(file)
    sql_con.query("INSERT INTO gallery (filename) VALUES (?)", [file.originalname], function(err, rows, fields) {
        if(err) throw err
        console.log('[+] gallery photo inserted')
    })

    res.status(200).json({msg:"Uploaded"})
})

// GET Gallery
app.get('/memorial/star-gallery', function(req, res){
    // TODO: insert SQL query
    sql_con.query("SELECT filename FROM gallery", function(err, rows, fields) {
        if(err) throw err

        console.log(rows)
        res.render('gallery', {PhotoData: rows})
    })
})


app.use('/memorial/style', express.static('style'))
app.use('/memorial/images', express.static('composed_images'))
app.use('/memorial/gallery', express.static('gallery'))
app.set('view engine', 'pug')
app.use(bodyParser.urlencoded({
    limit:'50mb', extended: true
}));

app.listen(2434)
