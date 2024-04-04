// create db config file for mongodb

const MongoClient = require("mongodb").MongoClient;

const url = "mongodb://localhost:27017";

exports.connect = async function () {
  try {
    const client = await MongoClient.connect(url, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    const db = client.db("sample_mflix");

    return db;
  } catch (error) {
    console.log(error);
  }
};
