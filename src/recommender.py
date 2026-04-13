from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv and returns a list of dicts with numeric fields cast to float/int."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # Skip any duplicate header rows embedded in the file
            if row["id"] == "id":
                continue
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user_prefs; returns (score, reasons) using the algorithm recipe."""
    score = 0.0
    reasons = []

    # Genre match: +2.0 exact, +1.0 if user's genre appears inside the song's genre string
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"genre match (+2.0)")
    elif user_prefs["favorite_genre"] in song["genre"]:
        score += 1.0
        reasons.append(f"close genre match (+1.0)")

    # Mood match: +1.0 exact only
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Energy similarity: +0.0–1.0 based on closeness
    energy_sim = round(1.0 - abs(song["energy"] - user_prefs["target_energy"]), 2)
    score += energy_sim
    reasons.append(f"energy similarity (+{energy_sim})")

    # Acoustic penalty: subtract acousticness when user dislikes acoustic
    if not user_prefs.get("likes_acoustic", True):
        penalty = round(song["acousticness"], 2)
        score -= penalty
        reasons.append(f"acoustic penalty (-{penalty})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song with score_song, sorts by score descending, and returns the top k as (song, score, explanation)."""
    # scored is a list of (song, score, reasons) for every track
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    # sorted() returns a new list; .sort() would mutate in place — sorted() is safer here
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    # Flatten reasons into a single explanation string for each result
    return [
        (song, score, " | ".join(reasons))
        for song, score, reasons in ranked[:k]
    ]
