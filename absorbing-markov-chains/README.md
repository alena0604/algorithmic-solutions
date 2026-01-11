## Goal

Compute the probability of ending in each absorbing state when starting from **state 0**.

---

## Solution

### Step 1. Identify transient and absorbing states

From the transition matrix:

- A state is **absorbing** if its row sums to 0  
- A state is **transient** if it has any outgoing probability  

Only transient states can lead to absorption, absorbing states are terminal.

---

### Step 2. Build the \(Q\) and \(R\) matrices

Reorder the states so that all transient states come first, followed by absorbing states.  
Then split the matrix into blocks:

- **\(Q\)** = transitions from transient → transient  
- **\(R\)** = transitions from transient → absorbing  

These two matrices capture:
- how the system moves before absorption (\(Q\))
- how it enters terminal states (\(R\))

---

### Step 3. Build the identity matrix \(I\)

Let \(I\) be the identity matrix with the same size as \(Q\).  
It represents “no movement” in the transient state space.

---

### Step 4. Solve for the absorption matrix \(B\)

The absorption probabilities are given by:

B = (I - Q)^{-1} R

Instead of explicitly computing the inverse, which is slow, we solve the equivalent linear system:

(I - Q) B = R

In code:

```doctest
b_matrix = (i_matrix - q_matrix).LUsolve(r_matrix)
```

Each row of B corresponds to a starting transient state.
Each column corresponds to an absorbing state.

### Output

The result is returned as:

```
result = [numerators, denominator]
```

This represents the exact probabilities for each absorbing state expressed as rational numbers.

---

### Explanation
 
https://alena408577.substack.com/p/solving-absorbing-markov-chains-python

