const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const cors = require("cors");
const mysql = require("mysql2");

const multer = require("multer");

// Multer configuration for storing files in memory
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

const db = mysql.createPool({
  host: "localhost",
  user: "root",
  password: "",
  database: "project_management",
});

app.use(cors());
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/api/get", (req, res) => {
  const id = req.params.id;

  const sqlGet = "select * from projects";
  db.query(sqlGet, id, (err, result) => {
    if (err) {
      console.log(err);
      res.status(500).send("Error fetching data from database");
    } else {
      if (result.length > 0) {
        const imageData = result[0].image_data.toString("base64");
        result[0].image_data = imageData;
        res.send(result);
      } else {
        res.status(404).send("Image not found");
      }
    }
  });
});

app.get("/api/get/:id", (req, res) => {
  const id = req.params.id;

  const sqlGet = "select * from projects where id=?";
  db.query(sqlGet, id, (err, result) => {
    if (err) {
      console.log(err);
      res.status(500).send("Error fetching data from database");
    } else {
      if (result.length > 0) {
        const imageData = result[0].image_data.toString("base64");
        result[0].image_data = imageData;
        res.send(result);
      } else {
        res.status(404).send("Image not found");
      }
    }
  });
});

app.put("/api/put",upload.single("image"), (req, res) => {
  const { id, brokerid, brokername } = req.body;
  const image_data = req.file.buffer;
  console.log(req.body,image_data);
  const sqlPut =
    "Update projects set id=?,brokerid=?,brokername=? ,image_data = ? where id=?";
  db.query(
    sqlPut,
    [id, brokerid, brokername, image_data, id],
    (err, result) => {
      if (err) {
        console.log(err);
      }
      res.send(result);
    }
  );
});
// Use upload middleware for handling file uploads
app.post("/api/post", upload.single("image"), (req, res) => {
  const { id, brokerid, brokername } = req.body;
  const image_data = req.file.buffer;
  console.log(image_data);

  const sqlInsert =
    "INSERT INTO projects (id, brokerid, brokername, image_data) VALUES (?, ?, ?, ?)";
  db.query(
    sqlInsert,
    [id, brokerid, brokername, image_data],
    (error, result) => {
      if (error) {
        console.log(error);
        res.status(500).send("Error inserting image into database");
      } else {
        res.status(200).send("Image uploaded successfully");
      }
    }
  );
});
app.delete("/api/remove/:id", (req, res) => {
  const { id } = req.params;
  const sqlDelete = "delete from projects where id=?";
  db.query(sqlDelete, id, (error, result) => {
    if (error) {
      console.log(error);
    }
  });
});

app.listen(5000, () => {
  console.log("Server running on port 5000");
});
