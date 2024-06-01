const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 5000;

app.use(bodyParser.json());

let claimedKeys = new Set();

function generateKey() {
    let key = '';
    for (let i = 0; i < 5; i++) {
        key += Math.floor(Math.random() * 10).toString();
    }
    return key;
}

app.get('/', (req, res) => {
    let key = generateKey();
    claimedKeys.add(key);
    res.json({ key: key });
});

app.post('/validate_key', (req, res) => {
    let key = req.body.key;
    if (claimedKeys.has(key)) {
        claimedKeys.delete(key);
        res.json({ valid: true });
    } else {
        res.json({ valid: false });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
