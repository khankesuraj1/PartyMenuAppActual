# Here are your Instructions
🍽️ PartyMenuAppActual
A full-featured web application for selecting dishes from a categorized party menu, with advanced search, filtering, and responsive design.

📖 Project Description
PartyMenuAppActual simplifies party planning by allowing users to browse, filter, and select dishes from multiple categories, eliminating the hassle of manual menu organization.

Target Users: Event planners, party hosts, catering services, and anyone organizing gatherings who need to efficiently manage food options.

🛠 Tech Stack
Frontend

React 19

React Router DOM 7.5.1

Tailwind CSS 3.4.17

Axios 1.8.4

CRACO 7.1.0

Backend

FastAPI 0.110.1

Pydantic 2.6.4+

Motor 3.3.1

Python 3.9+

Other

Yarn 1.22.22

Node.js 18+

MongoDB

Supervisorctl

⚙️ Installation
Prerequisites

Python 3.9+

Node.js 18+

Setup
# 1. Clone the repo
git clone <repository-url>
cd party-menu-app

# 2. Backend setup
cd backend
pip install -r requirements.txt

# 3. Frontend setup
cd frontend
yarn install

Environment Variables
# backend/.env
MONGO_URL=mongodb://localhost:27017
DB_NAME=party_menu_db

# frontend/.env
REACT_APP_BACKEND_URL=http://localhost:8001

▶️ Usage
Development
# Backend
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Frontend (new terminal)
cd frontend
yarn start

Production
sudo supervisorctl start all
sudo supervisorctl status

Access the App

Local: http://localhost:3000

✨ Features
4 Categories: Starter, Main Course, Dessert, Sides

18+ dishes with high-quality images

Real-time selection tracking

Advanced search (case-insensitive)

Veg/Non-Veg filters with icons

Ingredient details with quantities

Responsive design for all devices

Sticky selection summary

Combined filtering (search + category + veg/non-veg)

State persistence and error handling

📂 Project Structure

backend/                 # FastAPI backend
frontend/                # React frontend
tests/                   # Test files
backend_test.py          # API testing suite
test_result.md           # Test results
README.md                # Documentation
🧪 Testing
Backend

python backend_test.py
# 27/27 tests passed
Covers:

All API endpoints

Search & filtering

User selections

Error handling

Frontend

Category navigation

Search & filter

Dish selection/removal

Responsive design

🔗 API Endpoints
Base URL: /api

GET    /dishes
GET    /dishes/{dish_id}/ingredients
GET    /meal-types
GET    /selections/{user_id}
POST   /selections/{user_id}
DELETE /selections/{user_id}/{dish_id}
🤝 Contributing
Fork repo

Create branch (git checkout -b feature/Name)

Commit changes (git commit -m 'Add feature')

Push to branch

Open PR

📬 Contact & License
Issues via GitHub

Licensed under MIT

Acknowledgments

Unsplash (food images)

Tailwind CSS

React

FastAPI



Yarn

MongoDB
