# Reflection: Comparing User Profile Outputs

## High-Energy Pop Fan vs. Deep Intense Rock Head

Both profiles target high energy (0.85 and 0.92 respectively), so their #4 and #5 picks
overlap — *Rust and Thunder* and *Neon Cipher* appear for both purely because of energy
proximity, with no genre or mood match at all. The difference is at the top: the Pop Fan
gets *Sunrise City* and *Gym Hero*, while the Rock Head gets *Storm Runner*. This makes
sense because genre is the highest-weighted feature — once the catalog runs out of exact
genre matches, both profiles fall back to energy-only scoring and end up sharing the
same generic high-energy tail results.

## High-Energy Pop Fan vs. Sad Gym Rat (edge case)

These two profiles are almost identical except the Sad Gym Rat wants `mood: sad` instead
of `mood: happy`. But there are no "sad pop" songs in the catalog, so the mood bonus is
never awarded. The result: the Sad Gym Rat's top 5 are nearly the same as the Pop Fan's —
just with slightly shuffled scores because the mood bonus no longer separates *Sunrise City*
(happy) from *Gym Hero* (intense). A real person wanting sad music would get the same
upbeat recommendations as someone wanting happy music. This is a failure mode, not a
feature: the system is "confidently wrong" because it can only measure what the data
contains.

## Chill Lofi Listener vs. Niche Classical Acoustic Fan

Both profiles want low-energy, mellow music. The Lofi Listener gets a strong top 3
(*Library Rain*, *Midnight Coding*, *Focus Flow*) because the catalog has three lofi songs.
The Classical Fan gets a strong #1 (*Golden Hour Waltz*) because it is the only classical
song, but then the system has nothing left that matches — positions #2–#5 are filled with
ambient and lofi tracks selected purely on energy closeness. The output "feels" reasonable
at a glance (all calm, low-energy songs) but is actually misleading: the system is not
recommending music the user would enjoy, it is just recommending the least-wrong songs from
an insufficient catalog.

## What the Weight-Shift Experiment Revealed

When genre was halved (+1.0) and energy doubled (×2) for the Pop Fan profile:
- *Rooftop Lights* (indie pop, happy, 0.76 energy) jumped from #3 to #2, leapfrogging
  *Gym Hero* (pop, intense, 0.93 energy).
- The reason: *Rooftop Lights* scored a mood match (+1.0) that *Gym Hero* did not, and
  with genre worth less, that mood bonus made the difference.
- Songs with no genre match at all (hip hop, rock) rose to #4–#5 solely on energy grounds.

This experiment shows that the "right" weight depends entirely on what you think matters
more to a listener — genre loyalty or energy level. There is no neutral choice; every set
of weights encodes a designer assumption about human taste.

## Summary

The output across all five profiles confirmed that the recommender works as designed but
reveals a structural bias: **genre always dominates**. Profiles that have clear genre
representation in the catalog get excellent results; profiles that do not (or have
conflicting preferences like "sad" + "pop") get technically scored but emotionally wrong
results. This mirrors how real AI systems can be statistically "correct" and still
practically useless for edge-case users.
