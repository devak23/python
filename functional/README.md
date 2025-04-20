## Five tenets of functional programming

1. Computing problems consist of data and behavior
    * synonyms: state and operations; objects and methods; nouns and verbs
   
2. Immutability of data/state
    * once a variable is assigned to a value it should not be repointed; create a new one if required

3. Pure functions
    * Pure functions always produce same output for a given input.
    * Pure functions have no side effects and do NOT depend on external state or modify it any way

4. First class functions
    * functions can be passed around and manipulated just like other objects

5. Prefer recursion to loops
    * recursion is more declarative and avoids mutable state

6. Referential transparency
    * A function invocation is equivalent to its return value