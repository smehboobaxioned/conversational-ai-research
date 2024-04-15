// Importing necessary modules
import Path from "path";
import { getDocument, OPS } from "pdfjs-dist";
import sharp from "sharp";

// Function to export images from a PDF document
async function exportImages(src, dst = ".") {
  // Return a promise that resolves when the images are exported
  try {
    // Load the PDF document
    const doc = await getDocument(src).promise;
    return await processDoc(doc, dst);
  } catch (error) {
    console.error(error);
  }
}

// Function to process a PDF document and emit events for each image
async function processDoc(doc, dst) {
  const pageCount = doc._pdfInfo.numPages; // Get the number of pages
  const images = [];

  // Loop over each page
  for (let p = 1; p <= pageCount; p++) {
    const page = await doc.getPage(p); // Get the page
    const ops = await page.getOperatorList(); // Get the list of operations

    // Loop over each operation
    for (let i = 0; i < ops.fnArray.length; i++) {
      // Check if the operation is an image operation
      if (
        ops.fnArray[i] === OPS.paintImageXObject ||
        ops.fnArray[i] === OPS.paintInlineImageXObject
      ) {
        const name = ops.argsArray[i][0]; // Get the image name
        let img;

        // Get the image from the common objects or objects
        if (page.commonObjs.has(name)) {
          img = await page.commonObjs.get(name);
        } else if (page.objs.has(name)) {
          img = await page.objs.get(name);
        }

        // If the image exists
        if (img) {
          const { width, height, kind } = img; // Get the image properties
          const bytes = img.data.length; // Get the image data length
          const channels = bytes / width / height; // Calculate the number of channels where 1 represents grayscale, 2 represents grayscale with alpha, 3 represents RGB, and 4 represents RGBA

          // Check if the number of channels is valid
          if (![1, 2, 3, 4].includes(channels)) {
            throw new Error(
              `Invalid image channel: ${channels} for image ${name} on page ${page}`
            );
          }

          // Create the output file path
          const file = Path.join(dst, `${name}.png`);
          // Convert the image data to a PNG file
          await sharp(img.data, {
            raw: { width, height, channels },
          }).toFile(file);

          // Create an event with the image details
          const imgData = { name, kind, width, height, channels, bytes, file };
          images.push(imgData); // Add the event to the images array
        }
      }
    }
  }
  return images;
}

export { exportImages };
