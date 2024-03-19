const express = require('express');
const bodyParser = require('body-parser');
const multer = require('multer');
const path = require('path');

const app = express();
const port = 3000;

app.use(bodyParser.json());

// Set up multer for handling file uploads
const storage = multer.diskStorage({
    destination: './uploads/',
    filename: function (req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    },
});

const upload = multer({
    storage: storage,
}).single('image');

// Serve HTML file
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Handle dyslexia assessment submission
app.post('/submit-dyslexia-assessment', (req, res) => {
    // Use the upload middleware to handle the image file
    upload(req, res, (err) => {
        if (err) {
            console.error('Error uploading image', err);
            return res.status(500).json({ error: 'Error uploading image' });
        }

        const userAnswer = req.body.answer;
        const uploadedImage = req.file; // Assuming you have configured multer correctly

        // Perform any necessary processing with the received data
        // ...

        res.json({ message: 'Assessment submitted successfully' });
    });
});

// Serve uploaded images
app.use('/uploads', express.static('uploads'));

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
