const { PdfDocument } = require("@pomgui/pdf-tables-parser");
const fs = require("fs");

const pdf = new PdfDocument();

const loadPdf = async (pdf) => {
  const output = await pdf.load("TDS_Yulex Closed Cell Foams_Rev2.8.0-02-2024_ENGLISH.pdf");
  await output;
  console.log("out",output);
}
try {
  const loadedPdf =  loadPdf(pdf);
  console.log("loadedPdf",loadedPdf);
  fs.writeFileSync("table.json", JSON.stringify(loadedPdf, null, 2), "utf8");
} catch (err) {
  console.error(err);
}
