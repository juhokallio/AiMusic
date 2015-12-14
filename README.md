# AiMusic
Programmatic music composer application. 

Music is evaluated based on two different kind of approaches: First, based on the feedback collected by the web application tool, a measure for niceness is gathered. After all, music is for pleasing people, and it's hard to be completely cut off of the outer world. Second, an attempt is made to find real and objective creativity from music with bisociations. Connections and their level is measured, and this is an important part of the evaluation.

Based on the fitness function combining niceness classifiers from human feedback and bisociations from graph structure, a genetic algorithm is used to search the possibilities and compose. For speeding up the search, Markov chains from J.S. Bach music are used and music is modelled as motives, small elements that can be then repeated and varied.

Some of the created music samples can be listened from https://soundcloud.com/aimusicaloffering.
