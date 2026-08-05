# Rare Tree Locator
> *Identifying, tracking, and preserving rare and unique trees in urban Dhaka.*

[![Live Demo](https://img.shields.io/badge/Live-Website-brightgreen)](https://rare-tree-locator.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/tanishataranoon/Rare-tree-Locator)

---

## 🌐 Live Application
* **Website:** [rare-tree-locator.onrender.com](https://rare-tree-locator.onrender.com/)
* **Hosting Platform:** Render
* **Database Provider:** Supabase (PostgreSQL)



The Rare Tree Locator is a web-based platform designed to identify, track, and document rare and unique trees found within urban Dhaka. As the city continues to expand, many of its native or uncommon tree species face neglect and potential loss due to limited ecological awareness and the lack of accessible documentation tools. This project addresses that issue by combining technology and environmental awareness through a community-driven approach. Users can explore tree locations via an interactive map, contribute sightings with geotagged photos, and share information through blog posts. The system supports three types of users — Viewers, Contributors, and Admins, each with specific roles to ensure data quality and user engagement. Developed using Django (Python), HTML, LeafletJS, CSS, and JavaScript, the platform provides a scalable, interactive, and user-friendly solution that bridges the gap between citizens, researchers, and conservationists. Ultimately, the project promotes urban biodiversity awareness and citizen participation in preserving Dhaka’s natural heritage.

## Home Page
<img width="1917" height="911" alt="Screenshot 2026-08-05 143809" src="https://github.com/user-attachments/assets/05ee04fc-b501-4543-999f-812090a76491" />
<img width="1919" height="913" alt="Screenshot 2026-08-05 143816" src="https://github.com/user-attachments/assets/ca6774ca-8e33-4cc6-9b48-ff51d6040b71" />

## All the Rare Trees
<img width="1919" height="917" alt="Screenshot 2026-08-05 143829" src="https://github.com/user-attachments/assets/c9c419e0-a120-4f3d-81c2-f65036672a75" />

## See your favourite blogs
<img width="1919" height="908" alt="Screenshot 2026-08-05 144200" src="https://github.com/user-attachments/assets/7d9f3313-1eb7-4c07-9822-99d3def3b6f5" />

## You can add a rare tree & be a contributor
<img width="1919" height="918" alt="Screenshot 2026-08-05 143857" src="https://github.com/user-attachments/assets/c3907f55-74c8-4e92-af8d-709e9390c28f" />

## 📌 Project Overview
* **Target Region:** Urban Dhaka, Bangladesh
* **Course:** CSE 314 - Software Engineering Lab
* **Institution:** University of Asia Pacific
* **Technology Stack:** Python, Django, LeafletJS, HTML/CSS, JavaScript, PostgreSQL (Supabase)

---

## 📑 Table of Contents
1. [Introduction & Motivation](#-introduction--motivation)
2. [Problem Statement](#-problem-statement)
3. [Literature Review & Comparison](#-literature-review--comparison)
4. [Key Features & Roles](#-key-features--roles)
5. [System Architecture & Deployment](#-system-architecture--deployment)
6. [Tech Stack & Dependencies](#-tech-stack--dependencies)
7. [Installation & Setup](#-installation--setup)
8. [Testing & Quality Assurance](#-testing--quality-assurance)
9. [Project Management & Team](#-project-management--team)

---

## 🌿 Introduction & Motivation
The **Rare Tree Locator** bridges the gap between citizens, researchers, and conservationists by recording, preserving, and raising awareness about Dhaka's rare trees.

* **Preserve Ecological Memory:** Capture location-based urban flora data before it disappears[cite: 2].
* **Citizen Science:** Allow non-experts to contribute geotagged photos and sightings[cite: 2].
* **Local Context:** Address urban Dhaka's specific biodiversity needs unlike global platforms[cite: 2].

---

## 🚨 Problem Statement
Unchecked urban expansion in Dhaka is leading to rapid green space loss[cite: 2]. Existing plant identification tools (e.g., PlantNet, iNaturalist) are global and lack local context or dedicated map-based urban tree tracking for Bangladesh[cite: 2].

---

## 📊 Literature Review & Comparison

| Feature | Rare Tree Locator | PlantNet | iNaturalist | Flora of Bangladesh |
| :--- | :---: | :---: | :---: | :---: |
| **Focus** | Urban Trees (Dhaka) | All Plants | All Organisms | Native Trees |
| **Map-Based Tracking** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Geotagged Observations**| ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Role Moderation** | ✅ Yes | ❌ No | ⚠️ Limited | ❌ No |
| **Local Community Focus**| ✅ High | ❌ Low | ❌ Low | ⚠️ Medium |

---

## 👥 Key Features & Roles

### 👁️ Viewers
* Interactive LeafletJS map search and filter[cite: 2].
* Comprehensive tree profiles (species, habitat, rarity, GPS coordinates)[cite: 2].
* Request identification for unknown trees[cite: 2].

### ✍️ Contributors
* Submit geotagged tree sightings and photos[cite: 2].
* Post blog updates, seasonal updates, and conservation stories[cite: 2].
* Answer pending identification requests from Viewers[cite: 2].

### 🛡️ Admins
* Approve or reject user-submitted tree data and blogs[cite: 2].
* Manage user roles and system databases[cite: 2].

---

## 🏗️ System Architecture & Deployment
The system uses Django's **Model-View-Template (MVT)** design pattern[cite: 2], deployed using cloud services for production:

* **Web Service:** Deployed on **Render** as a web service.
* **Database Management:** Connected to **Supabase** for fully managed PostgreSQL hosting.

### Modular Applications
* **`MyApp`**: Handles user models, authentication, roles, and profiles[cite: 2].
* **`TreeApp`**: Manages tree data, requests, answers, and mapping coordinates[cite: 2].
* **`BlogApp`**: Handles posts, comments, nested replies, notifications, and bookmarks[cite: 2].
* **`DonationApp`**: Integrates SSLCommerz payment gateway for conservation funding[cite: 2].

---

## 💻 Tech Stack & Dependencies

* **Backend Framework:** Django 5.2+, Python[cite: 2]
* **Frontend:** HTML5, CSS3, JavaScript, Leaflet.js[cite: 2]
* **Database & Hosting:** PostgreSQL (Supabase), Render, Django Import-Export, Unfold Admin[cite: 2]
* **Testing:** Pytest, Selenium WebDriver[cite: 2]
* **Payments:** SSLCommerz Gateway Integration[cite: 2]

---

## ⚙️ Installation & Setup

```bash
# 1. Clone repository
git clone [https://github.com/tanishataranoon/Rare-tree-Locator.git](https://github.com/tanishataranoon/Rare-tree-Locator.git)
cd Rare-tree-Locator

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables (.env)
# DATABASE_URL=postgresql://user:password@aws-0-region.pooler.supabase.com:6543/postgres

# 5. Database migrations & setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 6. Run local development server
python manage.py runserver
