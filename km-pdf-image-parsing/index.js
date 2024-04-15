import fs from 'fs';
import { exportImages } from './export.js';
import { fileURLToPath } from 'url';
import path, { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const outputDir = path.join(__dirname, 'output');

async function createDirectoryAndExportImages() {
    try {
        await fs.promises.mkdir(outputDir, { recursive: true });
        const imageArray = await exportImages(path.join(__dirname, 'drylab.pdf'), outputDir);
        console.log('Exported', imageArray.length, 'images');
    } catch (error) {
        console.error(error);
    }
}

createDirectoryAndExportImages();