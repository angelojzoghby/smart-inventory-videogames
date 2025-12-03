📦 Smart Inventory System — Multimedia Database & Image Processing Project

Fall 2025 / 2026 — Faculty of Engineering, Department of Computer & Communication
Based on the project description:

🚀 Overview

This project is a Custom Smart Inventory System designed to automate product recognition and pricing using Machine Learning.
The system allows the user to upload a product image → classify it → predict its price → and manage inventory items efficiently.

📁 Folder Structure (Main Deliverables)
📄 docs/

Contains the PowerPoint Presentation required for the submission, including:

Backend architecture & APIs

Frontend UI walkthrough

Database schema & image storage

AI model selection + justification

Training pipeline & augmentations

🧠 ml/

Contains both AI models:

1️⃣ Image Classification Model (CNN-based)

Fine-tuned pretrained model (EfficientNet-B0)

Training notebook + preprocessing

Data augmentation justification

Saved model weights

2️⃣ Price Prediction Model (Regression)

ML model trained for price prediction (Random Forest)

Training code + preprocessing

Final serialized model

Both models are stored here as required by the deliverables.

🖥️ backend/

Contains the backend built with FastAPI, including:

RESTful API layer

Endpoints for image upload, classification, price prediction & inventory CRUD

Model loading + inference integration

MongoDB connection

GridFS

This folder includes all Python backend files and API logic.

🌐 frontend/

Contains the React.js (Vite) frontend, including:

Image upload UI

Classification + predicted price display

Editable price & quantity

Inventory dashboard

API integration with FastAPI