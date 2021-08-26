var express = require("express")
var app = express()
var db = require("./database.js")
var md5 = require("md5")

var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({
    extended: false
}));
app.use(bodyParser.json());

var HTTP_PORT = 8000

function access_control_origin(req, res, next) {
    console.log("access control allow origin handler middleware");
    res.header('Access-Control-Allow-Origin', "*");
    next();
}

function acess_control_headers(req, res, next) {
    console.log("access control allow headers handler middleware");
    res.header('Access-Control-Allow-Headers', "*");
    next();
}

var access_control_mw = [access_control_origin, acess_control_headers]

// Start server
app.listen(HTTP_PORT, () => {
    console.log("Server running on port %PORT%".replace("%PORT%", HTTP_PORT))
});

let sql_query = NaN;
let sql_params = NaN;

function sql_mng(req, res) {
    db.get(sql_query, sql_params, (err, row) => {
        if (err) {
            res.status(400).json({
                "error": err.message
            });
            return;
        }
        res.json({
            "message": "success",
            "data": row
        })
    });
}

app.get("/api/prod/:id", access_control_mw, (req, res, next) => {

  sql_query = "select * from prod where product_id = ?"
  sql_params = [req.params.id]
  next();

}, sql_mng);

app.get("/api/users/:id", access_control_mw, (req, res, next) => {

  sql_query = "select * from users where hash = ?"
  sql_params = [req.params.id]
  next();

}, sql_mng );

app.get("/api/reccom/:id", access_control_mw, (req, res, next) => {

  sql_query = "select * from reccom where user_id = ?"
  sql_params = [req.params.id]
  next();

}, sql_mng);

// Root path
app.get("/", (req, res, next) => {
    res.json({
        "message": "Ok"
    })
});