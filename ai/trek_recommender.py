import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


# =====================================================
# LOAD DATASET
# =====================================================

dataset_path = "ai/trek_dataset.csv"

treks = pd.read_csv(dataset_path)


# =====================================================
# FEATURES USED FOR RECOMMENDATION
# =====================================================

features = [
    "difficulty_score",
    "days",
    "distance_km",
    "altitude_m",
    "price",
    "rating"
]


# =====================================================
# PREPARE FEATURES
# =====================================================

X = treks[features]


# =====================================================
# SCALE FEATURES
# =====================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# =====================================================
# CREATE KNN MODEL
# =====================================================

model = NearestNeighbors(
    n_neighbors=5,
    metric="euclidean"
)

model.fit(X_scaled)


# =====================================================
# RECOMMEND TREKS
# =====================================================

def recommend_treks(
    difficulty_score,
    days,
    distance_km,
    altitude_m,
    price,
    rating
):

    user_preferences = [[
        difficulty_score,
        days,
        distance_km,
        altitude_m,
        price,
        rating
    ]]

    user_scaled = scaler.transform(
        user_preferences
    )

    distances, indexes = model.kneighbors(
        user_scaled
    )

    recommendations = []

    for distance, index in zip(
        distances[0],
        indexes[0]
    ):

        trek = treks.iloc[index]

        recommendations.append({
            "name": trek["name"],
            "location": trek["location"],
            "difficulty": trek["difficulty"],
            "days": int(trek["days"]),
            "distance_km": float(
                trek["distance_km"]
            ),
            "altitude_m": int(
                trek["altitude_m"]
            ),
            "price": float(
                trek["price"]
            ),
            "rating": float(
                trek["rating"]
            ),
            "distance": float(distance)
        })

    return recommendations


# =====================================================
# TEST THE MODEL
# =====================================================

if __name__ == "__main__":

    recommendations = recommend_treks(
        difficulty_score=2,
        days=1,
        distance_km=8,
        altitude_m=1500,
        price=1000,
        rating=4.7
    )

    print("\nRecommended Treks:\n")

    for trek in recommendations:

        print(
            trek["name"],
            "-",
            trek["difficulty"],
            "- ₹",
            trek["price"]
        )