"""Built-in knowledge base used by the tutor (RAG) before any uploads."""

SEED_DOCS: dict[str, str] = {
    "Python Basics": (
        "Python is an interpreted, high-level, general-purpose programming language. "
        "Variables are dynamically typed. Lists, dictionaries, sets and tuples are the core data structures.\n\n"
        "Functions are defined with def. List comprehensions build lists concisely, for example squares = [x*x for x in range(10)]."
    ),
    "Recursion": (
        "Recursion is when a function calls itself on a smaller version of the problem. Every recursive function needs a base case "
        "that stops the recursion and a recursive case that moves towards it.\n\n"
        "Example: factorial(n) = n * factorial(n-1) with factorial(0) = 1. Deep recursion can overflow the call stack."
    ),
    "Dynamic Programming": (
        "Dynamic Programming (DP) solves problems by breaking them into overlapping subproblems and storing results so each is computed once. "
        "There are two styles: top-down memoization and bottom-up tabulation.\n\n"
        "Classic examples: Fibonacci numbers, 0/1 knapsack, longest common subsequence. Start by defining the state, then the recurrence, then the base cases."
    ),
    "SQL": (
        "SQL is the language for querying relational databases. SELECT reads rows, WHERE filters them, GROUP BY aggregates, "
        "and JOIN combines tables on matching keys.\n\n"
        "An INNER JOIN keeps only matching rows; a LEFT JOIN keeps every row from the left table. Indexes speed up lookups."
    ),
    "Statistics": (
        "Statistics summarises and draws conclusions from data. The mean is the average, the median is the middle value and the standard deviation "
        "measures spread. A p-value is the probability of seeing results at least as extreme as observed if the null hypothesis were true.\n\n"
        "Correlation does not imply causation."
    ),
    "Probability": (
        "Probability measures how likely an event is, between 0 and 1. Independent events satisfy P(A and B) = P(A) * P(B). "
        "Conditional probability P(A|B) = P(A and B) / P(B).\n\n"
        "Bayes' theorem updates beliefs with evidence: P(A|B) = P(B|A) * P(A) / P(B)."
    ),
    "MapReduce": (
        "MapReduce is a programming model for processing large datasets in parallel on a cluster. The map step turns input into key-value pairs; "
        "the shuffle groups pairs by key; the reduce step aggregates each group.\n\n"
        "Hadoop is an open-source framework that implements MapReduce on top of the HDFS distributed file system."
    ),
    "Neural Networks": (
        "A neural network is a stack of layers of connected units. Each unit computes a weighted sum of its inputs and applies a non-linear activation. "
        "Training uses backpropagation to compute gradients and gradient descent to update the weights.\n\n"
        "Overfitting happens when a model memorises training data; regularisation and more data help."
    ),
    "Bayesian Knowledge Tracing": (
        "Bayesian Knowledge Tracing (BKT) is a Hidden Markov Model that estimates whether a student has mastered a skill. "
        "It has four parameters: initial knowledge, learning rate, guess and slip probabilities.\n\n"
        "After each answer the model updates the probability of mastery using Bayes' rule. Deep Knowledge Tracing replaces this with an LSTM."
    ),
    "Forgetting Curve": (
        "The forgetting curve describes how memory decays over time, commonly modelled as R = exp(-t/S), where t is the time since review and S is stability. "
        "Spaced repetition reviews material just before it is forgotten, increasing S each time."
    ),
}
