# AiMusic

A music composing program. Work in progress.

## The Search for Pure Art

J.S. Bach is my gold standard for art as its barest. It is abstract and self-contained - a single piece can be listened without any context, in any century. Music with lyrics makes direct connections to our lifes through words and concepts, but with Bach we have captured art to a lot smaller space.

One way to understand creativity is to think of it as connections. This thinking was formalized by Arthur Koestler in his book The Act of Creation. He introduced the concept bisociation, meaning a strange connection. The idea is that ordinary associations don't make art, but that when we can connect two things in an original way, something strange happens.

## Programmatic Music Composer Application. 

Music is evaluated based on two different kind of approaches: First, based on the feedback collected by the web application tool, a measure for niceness is gathered. After all, music is for pleasing people, and it's hard to be completely cut off of the outer world. Second, an attempt is made for finding real and objective creativity from music with bisociations. We calculate the score of the connections found from single piece of music. The algorithms origin from the BISON project (http://www.cs.helsinki.fi/group/bison/) and the research on finding bisociations from graph structures.

Based on the fitness function combining niceness classifiers from human feedback and bisociations from the graph structure of the music, a genetic algorithm is used to search the possibilities and compose music. For speeding up the search, Markov chains from J.S. Bach music are used and music is modelled as motives, small elements that can be then repeated and varied.

Some of the created music samples can be listened from https://soundcloud.com/aimusicaloffering.
