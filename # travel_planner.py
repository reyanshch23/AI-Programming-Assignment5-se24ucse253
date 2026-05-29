# travel_planner.py
# A simple rule-based AI travel planner that uses a local knowledge base
# (simulates reusing existing ontologies like tourist places, food, costs)

# --- Knowledge Base ---

PLACES_KB = {
    "Paris": {
        "country": "France",
        "type": ["city", "cultural"],
        "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"],
        "avg_daily_cost_usd": 200,
        "best_season": ["spring", "fall"],
        "cuisine": ["French", "Crepes", "Wine"],
        "languages": ["French"]
    },
    "Goa": {
        "country": "India",
        "type": ["beach", "party", "relaxation"],
        "attractions": ["Calangute Beach", "Dudhsagar Falls", "Old Goa Churches"],
        "avg_daily_cost_usd": 60,
        "best_season": ["winter"],
        "cuisine": ["Seafood", "Vindaloo", "Bebinca"],
        "languages": ["Konkani", "English"]
    },
    "Kyoto": {
        "country": "Japan",
        "type": ["cultural", "historical", "nature"],
        "attractions": ["Fushimi Inari", "Arashiyama Bamboo Grove", "Kinkaku-ji"],
        "avg_daily_cost_usd": 150,
        "best_season": ["spring", "fall"],
        "cuisine": ["Kaiseki", "Matcha sweets", "Tofu cuisine"],
        "languages": ["Japanese"]
    },
    "New York": {
        "country": "USA",
        "type": ["city", "cultural", "shopping"],
        "attractions": ["Central Park", "Statue of Liberty", "Times Square"],
        "avg_daily_cost_usd": 250,
        "best_season": ["spring", "fall", "summer"],
        "cuisine": ["Pizza", "Bagels", "International"],
        "languages": ["English"]
    },
    "Cape Town": {
        "country": "South Africa",
        "type": ["nature", "adventure", "beach"],
        "attractions": ["Table Mountain", "Robben Island", "Cape of Good Hope"],
        "avg_daily_cost_usd": 100,
        "best_season": ["summer"],
        "cuisine": ["Braai", "Bobotie", "Seafood"],
        "languages": ["English", "Afrikaans"]
    }
}

FOOD_KB = {
    "vegetarian": ["Kyoto", "Paris"],
    "seafood lover": ["Goa", "Cape Town"],
    "street food": ["Goa", "New York"],
    "fine dining": ["Paris", "New York", "Kyoto"]
}

ACTIVITY_KB = {
    "adventure": ["Cape Town", "Goa"],
    "history": ["Kyoto", "Paris", "New York"],
    "beach": ["Goa", "Cape Town"],
    "shopping": ["New York", "Paris"],
    "nature": ["Kyoto", "Cape Town"]
}

# --- Recommendation Engine ---

def recommend_places(interests, food_pref, season, budget_per_day):
    scores = {place: 0 for place in PLACES_KB}

    for interest in interests:
        interest = interest.lower()
        if interest in ACTIVITY_KB:
            for place in ACTIVITY_KB[interest]:
                scores[place] += 2

    if food_pref and food_pref.lower() in FOOD_KB:
        for place in FOOD_KB[food_pref.lower()]:
            scores[place] += 1

    for place, info in PLACES_KB.items():
        if season.lower() in info["best_season"]:
            scores[place] += 1
        if info["avg_daily_cost_usd"] <= budget_per_day:
            scores[place] += 1

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [p for p, s in ranked if s > 0]

def generate_tour_plan(place, days):
    if place not in PLACES_KB:
        print(f"Sorry, no data found for {place}.")
        return

    info = PLACES_KB[place]
    attractions = info["attractions"]
    daily_cost = info["avg_daily_cost_usd"]

    print(f"\n===== Tour Plan: {place}, {info['country']} =====")
    print(f"Duration     : {days} days")
    print(f"Est. Budget  : ~${daily_cost * days} USD (${daily_cost}/day)")
    print(f"Best season  : {', '.join(info['best_season'])}")
    print(f"Local cuisine: {', '.join(info['cuisine'])}")
    print(f"Languages    : {', '.join(info['languages'])}")
    print()
    print("Day-by-Day Plan:")

    for day in range(1, days + 1):
        print(f"  Day {day}:")
        idx = (day - 1) % len(attractions)
        print(f"    Morning  : Visit {attractions[idx]}")
        print(f"    Afternoon: Explore local {info['cuisine'][(day-1) % len(info['cuisine'])]} cuisine")
        if day % 2 == 0:
            print(f"    Evening  : Free time / shopping")
        else:
            print(f"    Evening  : Local cultural experience")

    print()
    print(f"Total Estimated Cost: ~${daily_cost * days} USD (excluding flights)")

def main():
    print("===== AI Travel Planner =====")
    print("Available interests:", list(ACTIVITY_KB.keys()))
    print("Available food prefs:", list(FOOD_KB.keys()))
    print()

    # --- Test case 1: budget beach trip in winter ---
    print("--- User Profile 1: Beach lover, seafood, winter, budget $80/day ---")
    results = recommend_places(
        interests=["beach", "adventure"],
        food_pref="seafood lover",
        season="winter",
        budget_per_day=80
    )
    print("Recommended destinations:", results)
    if results:
        generate_tour_plan(results[0], days=5)

    # --- Test case 2: history + culture, fine dining, fall, no budget limit ---
    print("\n--- User Profile 2: History buff, fine dining, fall, budget $300/day ---")
    results = recommend_places(
        interests=["history", "shopping"],
        food_pref="fine dining",
        season="fall",
        budget_per_day=300
    )
    print("Recommended destinations:", results)
    if results:
        generate_tour_plan(results[0], days=7)

if __name__ == '__main__':
    main()