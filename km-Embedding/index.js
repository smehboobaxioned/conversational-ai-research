/*
  get the data from json
  api to populate the data in the db while converting the data into vector data
  api to get the search data from the db
*/

const express = require("express");
const OpenAI = require("openai");
const app = express();
const connection = require("./dbConfig").connect();


const port = 3000;
const openai = new OpenAI({
  apiKey: "sk-<your-api-key>",
});


app.use(express.json());
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

app.post("/create/embeddings", async (req, res) => {
  try {
    const db = await connection;
    const { data } = req.body;
    for (const element of data) {
      // console.log(element);
      const embedding = await openai.embeddings.create({
        model: "text-embedding-3-small",
        input: element.plot,
        encoding_format: "float",
      });

      await db.collection("embedded_movie").insertOne({
        plot: element.plot,
        title: element.title,
        embedded_plot: embedding.data[0].embedding,
      });
    }

    console.log("Done");

    res.status(200).send("Embedding created");
  } catch (error) {
    console.log(error);
    res.status(500).send("Internal Server Error");
  }
});

app.post("/search/embeddings", async (req, res) => {
  try {
    const db = await connection;

    const { query } = req.body;

    const embedding = await openai.embeddings.create({
      model: "text-embedding-3-small",
      input: query,
      encoding_format: "float",
    });

    const result = await db
      .collection("embedded_movie")
      .aggregate([
        {
          $vectorSearch: {
            index: "movie_plot_embedding_index",
            path: "embedded_plot",
            queryVector: embedding.data[0].embedding,
            numCandidates: 100,
            limit: 5,
          },
        },
        {
          $project: {
            title: 1,
            plot: 1,
            _id: 0,
          },
        },
      ])
      .toArray();

    console.log("Done");

    res.status(200).send(result);
  } catch (error) {
    console.log(error);
    res.status(500).send("Internal Server Error");
  }
});
