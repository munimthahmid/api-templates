const express = require('express');
const cors = require('cors');
const { Translate } = require('@google-cloud/translate').v2;
require('dotenv').config();

const app = express();
const port = 8000;

// Enable CORS for your React app
app.use(cors());
app.use(express.json());

// Initialize Google Translate
const translate = new Translate({
  projectId: process.env.GOOGLE_CLOUD_PROJECT_ID,
  key: process.env.GOOGLE_CLOUD_API_KEY
});

app.post('/speech/translate', async (req, res) => {
  try {
    const { text } = req.body;
    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }

    const [translation] = await translate.translate(text, 'bn');
    res.json({ translation });
  } catch (error) {
    console.error('Translation error:', error);
    res.status(500).json({ error: 'Translation failed' });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
