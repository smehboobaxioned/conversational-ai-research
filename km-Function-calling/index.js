/*
  get the data from json
  api to populate the data in the db while converting the data into vector data
  api to get the search data from the db
*/

const express = require("express");
const OpenAI = require("openai");
const fetch = require("node-fetch");
const app = express();

const port = 3000;
const openai = new OpenAI({
  apiKey: "sk-<your-api-key>",
});

app.use(express.json());
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

async function liveWeather(city) {
  const api = "your-api-key";
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${api}&units=metric`;
  const response = await fetch(url);
  const weatherData = await response.json();
  return weatherData;
}

const liveWeatherFunctionSpecs = {
  name: "liveWeather",
  description: "Get the live weather data",
  inputs: ["query"],
  outputs: ["weatherData"],
  function: liveWeather,
  parameters: {
    type: "object",
    properties: {
      city: {
        type: "string",
        description: "The city to get the weather data",
      },
    },
    },
    required: ["city"],
};

app.post("/", async (req, res) => {
  try {
    const { query } = req.body;

    const messages = [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: query },
    ]

    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo-0125",
      messages,
      functions: [liveWeatherFunctionSpecs],
    });

    const responseMessage = response.choices[0].message;
    messages.push(responseMessage);

    if(responseMessage.function_call?.name === "liveWeather") {
      const args = JSON.parse(responseMessage.function_call.arguments);
      const city = args.city;
      const weatherData = await liveWeather(city);

      messages.push({
        role: "function",
        name: "liveWeather",
        content: JSON.stringify(weatherData),
      });

    }

    const result = await openai.chat.completions.create({
      model: "gpt-3.5-turbo-0125",
      messages,
      functions: [liveWeatherFunctionSpecs],
    });

    res.status(200).send(result.choices[0].message.content);
  } catch (error) {
    console.log(error);
    res.status(500).send("Internal Server Error");
  }
});
