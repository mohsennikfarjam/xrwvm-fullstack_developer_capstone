const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').json());

const reviews_data = JSON.parse(fs.readFileSync("./data/reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("./data/dealerships.json", 'utf8'));

app.get('/fetchReviews', (req, res) => res.json(reviews_data['reviews']));
app.get('/fetchReviews/dealer/:id', (req, res) => {
    const filtered = reviews_data['reviews'].filter(r => r.dealership == req.params.id);
    res.json(filtered);
});
app.get('/fetchDealers', (req, res) => res.json(dealerships_data['dealerships']));
app.get('/fetchDealers/:state', (req, res) => {
    const filtered = dealerships_data['dealerships'].filter(d => d.state == req.params.state);
    res.json(filtered);
});
app.get('/fetchDealer/:id', (req, res) => {
    const filtered = dealerships_data['dealerships'].filter(d => d.id == req.params.id);
    res.json(filtered[0] || {});
});

app.listen(port, () => console.log(`Server is running on http://localhost:${port}`));
