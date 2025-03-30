# 🌊 OceanPulse: Connecting Illegal Fishing Detection with Marine Ecosystem Impact

A 36-hour hackathon project built at [HackPrinceton], OceanPulse detects illegal fishing vessels using satellite imagery and correlates their behavior with fish migration data to visualize ecological impact zones in real-time. 🌐🐟

---

## ⚡ TL;DR

- Illegal fishing threatens marine ecosystems globally — accounting for up to 20% of all caught fish.
- Satellite data is useful for spotting ships, but doesn’t account for ecological impact.
- OceanPulse combines **vessel detection** with **fish migration models** to assess and visualize harm to biodiversity.
- Integrates AI-generated fish impact reports via the **Gemini API** for added insight.
- Everything you sea here was built in 36 hours!

---

## 🧠 What We Built

1. **Ship Detection Module**  
   A neural network to detect fishing vessels using satellite imagery, trained on real + synthetic data.

2. **Fish Migration Correlation Engine**  
   Matches fishing vessel presence to migratory routes using OBIS and NOAA datasets.

3. **LLM-Generated Ecological Summaries**  
   Users can input a custom prompt (e.g., a fish species or threat), and get AI-generated insights using the **Gemini API**.

4. **Interactive Dashboard (Frontend)**  
   A live, map-based visualization of ship hotspots and their ecological impact — coming from our Flask API.

---

## 🔧 Backend Features (This Repo)

This repo includes the full Flask backend used for the OceanPulse API:

| Endpoint                          | Method | Description                                              |
|----------------------------------|--------|----------------------------------------------------------|
| `/data/<species>`                | GET    | Returns occurrence points for a given species            |
| `/data/<species>/<month>/<year>`| GET    | Filters occurrence data by month/year                    |
| `/data/<species>/<year>`        | GET    | Filters occurrence data by year                          |
| `/generate`                      | POST   | Returns Gemini-generated response for a user prompt      |

Uses:
- [OBIS](https://obis.org) APIs for marine species data
- [Google Gemini](https://deepmind.google/technologies/gemini/) API for AI insights
- `flask`, `requests`, `dotenv`, and `flask-cors`

---

## 📡 Key Datasets

- **OBIS Marine Biodiversity** — Species occurrence points
- **NOAA Fisheries** — Fish stock + migration data
- **Global Fishing Watch** — AIS tracking for 60,000+ vessels
- **Dark Vessel Dataset** — 55,000+ AIS gap records for suspected illegal activity

---

## 🔬 Example Usage

### 🔎 Species Occurrence
```bash
curl http://localhost:5000/data/Thunnus%20albacares
