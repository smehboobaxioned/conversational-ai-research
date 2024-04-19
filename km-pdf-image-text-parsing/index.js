import fs from 'fs';
import { exportImages, extractText } from './export.js';
import { fileURLToPath } from 'url';
import path, { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const outputDir = path.join(__dirname, 'output');

async function createDirectoryAndExportImages() {
    try {
        await fs.promises.mkdir(outputDir, { recursive: true });
        // const imageArray = await exportImages(path.join(__dirname, 'Yulex Foam Technical Brief (1).pdf'), outputDir);
        // const text = await extractText(path.join(__dirname, 'Yulex Foam Technical Brief (1).pdf'));
        const imageArray = await exportImages(path.join(__dirname, 'annie-8x11.pdf'), outputDir);
        const text = await extractText(path.join(__dirname, 'annie-8x11.pdf'));
        fs.writeFileSync(path.join(outputDir, 'text.txt'), text);
        console.log('Exported', imageArray.length, 'images');
    } catch (error) {
        console.error(error);
    }
}

createDirectoryAndExportImages();