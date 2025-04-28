const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(express.json()); // Use express.json() for better parsing of JSON

const reviews_data = JSON.parse(fs.readFileSync('reviews.json', 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync('dealerships.json', 'utf8'));

// MongoDB connection with error handling
mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' })
  .then(() => console.log("Connected to MongoDB"))
  .catch(err => console.error("Error connecting to MongoDB", err));

// Importing the Mongoose models
const Reviews = require('./review');
const Dealerships = require('./dealership');

// Seeding data if collections are empty (improved)
Reviews.countDocuments().then(count => {
  if (count === 0) {
    Reviews.insertMany(reviews_data['reviews']);
  }
});

Dealerships.countDocuments().then(count => {
  if (count === 0) {
    Dealerships.insertMany(dealerships_data['dealerships']);
  }
});

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const reviews = await Reviews.find();
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const reviews = await Reviews.find({ dealership: req.params.id });
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews for this dealer' });
  }
});

// Express route to fetch all dealerships with pagination
app.get('/fetchDealers', async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1; // Default to page 1 if no page is provided
    const limit = parseInt(req.query.limit) || 10; // Default to 10 items per page
    const dealerships = await Dealerships.find()
      .skip((page - 1) * limit) // Skip records for the current page
      .limit(limit); // Limit the number of records per page
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch dealerships by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealerships = await Dealerships.find({ state: req.params.state });
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch a specific dealership by its ID
// Express route to fetch a specific dealership by its custom `id`
app.get('/fetchDealer/:id', async (req, res) => {
    try {
      console.log("Fetching dealership with ID:", req.params.id); // Log the ID being passed
  
      // Find by the custom `id` field instead of MongoDB's _id
      const dealership = await Dealerships.findOne({ id: parseInt(req.params.id) }); // Query using custom `id`
  
      if (!dealership) {
        return res.status(404).json({ error: 'Dealer not found' });
      }
  
      res.json(dealership); // Send the dealership document
    } catch (error) {
      console.error("Error fetching dealership by ID:", error); // Log the error for debugging
      res.status(500).json({ error: 'Error fetching dealer by ID' });
    }
  });
  
// Express route to insert a review
app.post('/insert_review', async (req, res) => {
  const data = req.body;

  // Validate input data
  if (!data.name || !data.dealership || !data.review) {
    return res.status(400).json({ error: 'Missing required fields: name, dealership, and review' });
  }

  try {
    const documents = await Reviews.find().sort({ id: -1 }).limit(1);
    let new_id = documents.length > 0 ? documents[0].id + 1 : 1;

    const review = new Reviews({
      id: new_id,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
