"""
Command line runner for the Music Recommender Simulation.

Runs the recommender for multiple user profiles so results can be
compared side-by-side and evaluated for accuracy and bias.
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop Fan": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi Listener": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.38,
        "likes_acoustic": True,
    },
    "Deep Intense Rock Head": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "likes_acoustic": False,
    },
    # Adversarial: high energy but sad mood — conflicting preferences
    "Sad Gym Rat (edge case)": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    # Adversarial: no clear genre match in the catalog
    "Niche Classical Acoustic Fan": {
        "favorite_genre": "classical",
        "favorite_mood": "nostalgic",
        "target_energy": 0.20,
        "likes_acoustic": True,
    },
}


def print_results(profile_name: str, recommendations: list) -> None:
    """Prints a formatted recommendation block for one user profile."""
    print("\n" + "=" * 56)
    print(f"  Profile: {profile_name}")
    print("=" * 56)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f}")
        print(f"       Why:   {explanation}")
    print()


def main() -> None:
    """Loads the catalog once, then evaluates every profile and prints ranked results."""
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        recs = recommend_songs(user_prefs, songs, k=5)
        print_results(profile_name, recs)


if __name__ == "__main__":
    main()
