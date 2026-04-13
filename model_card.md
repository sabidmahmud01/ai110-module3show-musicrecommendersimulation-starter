# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder's job is to suggest the five most relevant songs from a small catalog given a
user's stated taste. It is a **content-based filtering** system: it compares song attributes
(genre, mood, energy, acousticness) directly against user preferences and returns the
closest matches. It does not learn from listening history or compare users to each other.

---

## 3. Data Used

- **Catalog size:** 17 songs in `data/songs.csv`
- **Features per song:** genre (text label), mood (text label), energy (0–1 float),
  tempo_bpm, valence, danceability, acousticness (0–1 floats)
- **Genres covered:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop,
  electronic, country, folk, metal, reggae, classical
- **Moods covered:** happy, chill, intense, focused, relaxed, moody, nostalgic, dreamy,
  soulful, playful, energetic, cinematic, melancholic
- **Limits:** Most genres have only 1–2 songs. There are no songs labeled "sad", "angry",
  or "romantic", so users who ask for those moods will always score 0 mood points.
  The dataset was not modified from the starter — no songs added or removed.

---

## 4. Algorithm Summary

Think of VibeFinder as a scorecard for every song in the catalog. For each track, it
calculates four numbers and adds them together:

1. **Genre points** — If the song's genre exactly matches what the user wants, add 2 points.
   If it's close (like "indie pop" when the user asked for "pop"), add 1 point. Otherwise 0.

2. **Mood points** — If the song's mood exactly matches, add 1 point. No partial credit.

3. **Energy closeness** — The closer the song's energy level is to the user's target, the
   more points it earns (up to 1 point). A song at exactly the right energy gets a full
   point; one that's very different gets close to zero.

4. **Acoustic penalty** — If the user said they dislike acoustic music, a small amount is
   subtracted based on how acoustic the song is. A heavily acoustic song loses more points.

All songs are ranked from highest score to lowest, and the top five are returned with a
plain-English explanation of exactly why each song scored what it did.

---

## 5. Observed Behavior / Biases

**Genre dominates the ranking.** Genre is worth 2 points — twice as much as mood (1 point)
and twice the maximum energy score (1 point). In practice, this means a song of the right
genre but the wrong mood will almost always beat a song of the wrong genre but the right
mood. For the "Sad Gym Rat" adversarial profile (pop genre + sad mood), the system
confidently recommended upbeat happy pop songs because "pop" was in the catalog but "sad
pop" was not. The user would get technically genre-correct but emotionally wrong results.

**Mood scoring is binary.** "Playful" and "happy" score the same as "melancholic" and
"happy" — both earn zero mood points even though the first pair is clearly more similar.

**Small catalog amplifies genre bias.** With 17 songs, a user whose preferred genre has
only one catalog entry (e.g., classical, reggae, country) gets a near-perfect #1 result
but then a completely irrelevant #2–#5. The system always returns 5 results even when
fewer than 5 songs are genuinely relevant.

**Weight sensitivity:** When genre was halved (+1.0) and energy doubled (×2.0) in an
experiment, the rankings changed significantly — confirming that the weights encode the
designer's assumptions about what matters, not any objective truth about musical taste.

---

## 6. Evaluation Process

Five user profiles were designed and tested:

| Profile | Intent | Top Result | Felt Accurate? |
|---|---|---|---|
| High-Energy Pop Fan | Normal use case | Sunrise City (pop, happy) | Yes |
| Chill Lofi Listener | Low-energy niche | Library Rain (lofi, chill) | Yes |
| Deep Intense Rock Head | High-energy niche | Storm Runner (rock, intense) | Yes |
| Sad Gym Rat | Adversarial — conflicting mood + energy | Gym Hero (pop, intense, not sad) | No |
| Niche Classical Acoustic Fan | Adversarial — tiny genre coverage | Golden Hour Waltz (classical) | Yes for #1 only |

One **weight-shift experiment** was also run: genre weight halved from +2.0 to +1.0 and
energy weight doubled from ×1.0 to ×2.0. Key finding: *Rooftop Lights* jumped from #3
to #2 for the Pop Fan, and off-genre songs with matching energy rose into the top 5.

The biggest surprise: the Classical Fan profile returned an excellent #1 result but then
completely ran out of relevant songs — positions #2–#5 were filled by low-energy ambient
and lofi tracks with no genre or mood connection, just similar energy. The system appeared
confident when it was actually guessing.

---

## 7. Intended Use and Non-Intended Use

### Intended Use

- Classroom exploration of how content-based recommender systems work
- Learning how scoring weights affect ranking outcomes
- Demonstrating transparency in AI decision-making through explainable score breakdowns

### Non-Intended Use

- **Not for real users.** The catalog is too small (17 songs) to surface meaningful variety.
- **Not a substitute for professional music curation.** The system has no understanding of
  lyric content, cultural context, artist intent, or listener history.
- **Not for sensitive emotional contexts.** A user seeking music to match a difficult
  emotional state (grief, anxiety) could receive entirely wrong recommendations because the
  catalog lacks those mood labels.
- **Not production-ready.** There is no user authentication, no persistent preferences, no
  feedback loop, and no protection against adversarial inputs.

---

## 8. Ideas for Improvement

1. **Expand the catalog to 100+ songs** so that every genre and mood has enough entries to
   fill a top-5 list with genuinely relevant results — not just energy-adjacent filler.

2. **Add partial mood credit** using a mood similarity table (e.g., "happy" and "playful"
   earn 0.5 points, "happy" and "melancholic" earn 0). This removes the binary cliff that
   causes similar moods to score identically to completely opposite ones.

3. **Add a diversity rule** that prevents more than 2 songs from the same genre appearing
   in the same top-5 list, so results feel more exploratory and less like a single-genre
   playlist.

---

## 9. Personal Reflection

**Biggest learning moment:** The weight-shift experiment was the clearest "aha" in the
whole project. I expected changing the numbers would tweak the rankings slightly. Instead,
it completely reordered the middle of the list and surfaced songs that had previously been
invisible. That one change made it obvious that a recommender system is not "discovering"
good matches — it is enforcing the designer's assumptions about what a good match looks
like. Every weight is a value judgment.

**How AI tools helped, and when I double-checked:** AI tools were genuinely useful for
generating boilerplate (CSV loading, sorting logic) and for suggesting adversarial test
cases I might not have thought of — like the "Sad Gym Rat" profile that exposed the mood
blindness problem. But I had to verify the scoring math myself. When I first ran the edge-
case profiles, the output looked reasonable at a glance, and I almost missed that the
Classical Fan's #2–#5 results were completely unrelated to classical music. AI tools tend
to produce plausible-looking outputs; checking whether they are *correct* still requires
human judgment.

**What surprised me about simple algorithms feeling like recommendations:** Even with four
basic rules and 17 songs, the output "feels" like a real recommendation when it works. The
pop fan profile returns exactly the songs a pop fan would want. This was surprising because
the algorithm has no understanding of music whatsoever — it just does arithmetic on labels.
Real music apps use much more complex methods but the fundamental pattern (score every item,
sort, return the top N) is the same. The "intelligence" is mostly in the data quality and
the weight choices, not in the algorithm.

**What I would try next:** I would add a feedback loop — let the user rate each
recommendation as "good" or "bad" and use those ratings to nudge the weights up or down
over time. This would turn VibeFinder from a static rule-based system into something that
actually learns from the user, which is how real collaborative filtering systems work. The
scoring recipe would stay the same; only the numbers would evolve.
