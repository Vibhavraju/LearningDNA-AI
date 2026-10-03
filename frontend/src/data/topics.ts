export interface TopicItem {
  id: string;
  name: string;
  subjectId: string;
  subjectName: string;
  description: string;
  prerequisites: string[]; // array of topic ids
  estimatedMinutes: number;
  skills: string[];
}

export interface SubjectItem {
  id: string;
  name: string;
  icon: string;
  color: string;
  description: string;
  topics: TopicItem[];
}

export const SUBJECTS: SubjectItem[] = [
  {
    id: 'python',
    name: 'Python Programming',
    icon: 'Terminal',
    color: 'from-blue-500 to-indigo-600',
    description: 'Core programming constructs, functions, data structures, and advanced recursion.',
    topics: [
      {
        id: 'py-basics',
        name: 'Python Syntax & Variables',
        subjectId: 'python',
        subjectName: 'Python Programming',
        description: 'Variables, data types, string manipulation, conditionals, and loops.',
        prerequisites: [],
        estimatedMinutes: 45,
        skills: ['Variable assignment', 'Type casting', 'Control flow', 'List indexing'],
      },
      {
        id: 'py-functions',
        name: 'Functions & Scope',
        subjectId: 'python',
        subjectName: 'Python Programming',
        description: 'Defining functions, arguments (*args, **kwargs), return values, lambda functions, and scope.',
        prerequisites: ['py-basics'],
        estimatedMinutes: 60,
        skills: ['Function definitions', 'Default args', 'Higher-order functions', 'Closures'],
      },
      {
        id: 'py-recursion',
        name: 'Recursion & Call Stacks',
        subjectId: 'python',
        subjectName: 'Python Programming',
        description: 'Recursive thinking, base cases, call stack mechanics, and tree traversal.',
        prerequisites: ['py-functions'],
        estimatedMinutes: 75,
        skills: ['Base case formulation', 'Call stack tracing', 'Divide and conquer'],
      },
      {
        id: 'py-dp',
        name: 'Memoization & Dynamic Programming',
        subjectId: 'python',
        subjectName: 'Python Programming',
        description: 'Optimizing recursive problems using top-down memoization and bottom-up tabulation.',
        prerequisites: ['py-recursion'],
        estimatedMinutes: 90,
        skills: ['Overlapping subproblems', 'Memoization dicts', 'Tabulation tables', 'Space optimization'],
      },
    ],
  },
  {
    id: 'sql',
    name: 'SQL & Databases',
    icon: 'Database',
    color: 'from-emerald-500 to-teal-600',
    description: 'Relational data modeling, querying, multi-table joins, and aggregations.',
    topics: [
      {
        id: 'sql-basics',
        name: 'SELECT, Filtering & Sorting',
        subjectId: 'sql',
        subjectName: 'SQL & Databases',
        description: 'Basic SELECT queries, WHERE filters, ORDER BY, LIMIT, and LIKE patterns.',
        prerequisites: [],
        estimatedMinutes: 40,
        skills: ['SELECT clauses', 'WHERE conditions', 'ORDER BY', 'NULL handling'],
      },
      {
        id: 'sql-joins',
        name: 'Multi-Table JOIN Operations',
        subjectId: 'sql',
        subjectName: 'SQL & Databases',
        description: 'INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN, and self-joins.',
        prerequisites: ['sql-basics'],
        estimatedMinutes: 60,
        skills: ['Foreign key relationships', 'INNER vs OUTER joins', 'Cross joins', 'Alias usage'],
      },
      {
        id: 'sql-aggregations',
        name: 'GROUP BY & Window Functions',
        subjectId: 'sql',
        subjectName: 'SQL & Databases',
        description: 'COUNT, SUM, AVG, GROUP BY, HAVING, and analytic window functions (ROW_NUMBER, RANK).',
        prerequisites: ['sql-joins'],
        estimatedMinutes: 70,
        skills: ['Aggregate functions', 'HAVING filtering', 'Window partitions', 'Cumulative metrics'],
      },
      {
        id: 'sql-design',
        name: 'Schema Design & Normalization',
        subjectId: 'sql',
        subjectName: 'SQL & Databases',
        description: 'Entity-relationship modeling, 1NF/2NF/3NF normalization, indexes, and constraints.',
        prerequisites: ['sql-aggregations'],
        estimatedMinutes: 80,
        skills: ['Normalization rules', 'Indexing strategies', 'Foreign keys', 'ACID transactions'],
      },
    ],
  },
  {
    id: 'statistics',
    name: 'Statistics & Probability',
    icon: 'BarChart2',
    color: 'from-amber-500 to-orange-600',
    description: 'Descriptive stats, distributions, probability theory, and statistical hypothesis testing.',
    topics: [
      {
        id: 'stats-basics',
        name: 'Descriptive Statistics & Dispersion',
        subjectId: 'statistics',
        subjectName: 'Statistics & Probability',
        description: 'Mean, median, mode, variance, standard deviation, interquartile ranges, and skewness.',
        prerequisites: [],
        estimatedMinutes: 45,
        skills: ['Central tendency', 'Standard deviation', 'IQR calculation', 'Outlier detection'],
      },
      {
        id: 'stats-probability',
        name: 'Probability Rules & Bayes Theorem',
        subjectId: 'statistics',
        subjectName: 'Statistics & Probability',
        description: 'Conditional probability, independent events, Bayes rule, and probability trees.',
        prerequisites: ['stats-basics'],
        estimatedMinutes: 65,
        skills: ['Joint probability', 'Conditional probability', 'Bayesian updating', 'Combinatorics'],
      },
      {
        id: 'stats-distributions',
        name: 'Distributions & Central Limit Theorem',
        subjectId: 'statistics',
        subjectName: 'Statistics & Probability',
        description: 'Normal, Binomial, Poisson distributions, Z-scores, and the Central Limit Theorem.',
        prerequisites: ['stats-probability'],
        estimatedMinutes: 75,
        skills: ['Normal distribution', 'Z-score standardization', 'CLT intuition', 'Sampling error'],
      },
      {
        id: 'stats-hypothesis',
        name: 'Hypothesis Testing & P-Values',
        subjectId: 'statistics',
        subjectName: 'Statistics & Probability',
        description: 'Null and alternative hypotheses, Type I/II errors, t-tests, ANOVA, and p-value interpretation.',
        prerequisites: ['stats-distributions'],
        estimatedMinutes: 90,
        skills: ['Null hypothesis testing', 'p-value interpretation', 'Confidence intervals', 't-tests'],
      },
    ],
  },
  {
    id: 'ml',
    name: 'Machine Learning',
    icon: 'Brain',
    color: 'from-purple-500 to-violet-600',
    description: 'Data preprocessing, supervised algorithms, unsupervised clustering, and evaluation metrics.',
    topics: [
      {
        id: 'ml-foundations',
        name: 'ML Foundations & Preprocessing',
        subjectId: 'ml',
        subjectName: 'Machine Learning',
        description: 'Train/test splitting, feature scaling, one-hot encoding, bias-variance tradeoff.',
        prerequisites: ['py-functions', 'stats-basics'],
        estimatedMinutes: 60,
        skills: ['Feature scaling', 'Train/test split', 'Bias-variance tradeoff', 'Overfitting detection'],
      },
      {
        id: 'ml-supervised',
        name: 'Supervised Learning & Classifiers',
        subjectId: 'ml',
        subjectName: 'Machine Learning',
        description: 'Linear regression, logistic regression, decision trees, random forests, and metrics (Precision, Recall, F1).',
        prerequisites: ['ml-foundations'],
        estimatedMinutes: 80,
        skills: ['Linear/logistic regression', 'Decision trees', 'Confusion matrix', 'ROC-AUC'],
      },
      {
        id: 'ml-unsupervised',
        name: 'Unsupervised Learning & Clustering',
        subjectId: 'ml',
        subjectName: 'Machine Learning',
        description: 'K-Means clustering, hierarchical clustering, and Principal Component Analysis (PCA).',
        prerequisites: ['ml-supervised'],
        estimatedMinutes: 75,
        skills: ['K-Means clustering', 'Elbow method', 'Dimensionality reduction', 'PCA variance ratio'],
      },
      {
        id: 'ml-neural-nets',
        name: 'Neural Networks & Deep Learning',
        subjectId: 'ml',
        subjectName: 'Machine Learning',
        description: 'Perceptrons, activation functions (ReLU, Sigmoid), backpropagation, and loss minimization.',
        prerequisites: ['ml-supervised'],
        estimatedMinutes: 100,
        skills: ['Forward propagation', 'Backpropagation', 'Activation functions', 'Gradient descent'],
      },
    ],
  },
  {
    id: 'dsa',
    name: 'Data Structures & Algorithms',
    icon: 'Layers',
    color: 'from-rose-500 to-pink-600',
    description: 'Big-O notation, linear structures, trees, graphs, sorting, and search algorithms.',
    topics: [
      {
        id: 'dsa-arrays',
        name: 'Arrays, Strings & Two Pointers',
        subjectId: 'dsa',
        subjectName: 'Data Structures & Algorithms',
        description: 'Array memory layout, Big-O complexity, sliding window, and two-pointer techniques.',
        prerequisites: ['py-basics'],
        estimatedMinutes: 50,
        skills: ['Big-O analysis', 'Sliding window', 'Two pointers', 'In-place reversal'],
      },
      {
        id: 'dsa-linked-lists',
        name: 'Linked Lists, Stacks & Queues',
        subjectId: 'dsa',
        subjectName: 'Data Structures & Algorithms',
        description: 'Singly/doubly linked lists, cycle detection (Floyd’s algorithm), LIFO stacks, FIFO queues.',
        prerequisites: ['dsa-arrays'],
        estimatedMinutes: 70,
        skills: ['Pointer manipulation', 'Stack operations', 'Cycle detection', 'Queue buffers'],
      },
      {
        id: 'dsa-trees',
        name: 'Binary Trees & BST Traversals',
        subjectId: 'dsa',
        subjectName: 'Data Structures & Algorithms',
        description: 'Binary search trees, DFS traversals (in-order, pre-order, post-order), and BFS level-order.',
        prerequisites: ['dsa-linked-lists', 'py-recursion'],
        estimatedMinutes: 85,
        skills: ['Tree recursion', 'In-order traversal', 'BFS queue pattern', 'BST search property'],
      },
      {
        id: 'dsa-graphs',
        name: 'Graph Algorithms (BFS/DFS & Shortest Path)',
        subjectId: 'dsa',
        subjectName: 'Data Structures & Algorithms',
        description: 'Adjacency lists, BFS/DFS traversal, cycle detection in graphs, and Dijkstra’s algorithm.',
        prerequisites: ['dsa-trees'],
        estimatedMinutes: 95,
        skills: ['Adjacency representations', 'Graph BFS/DFS', 'Topological sort', 'Dijkstra shortest path'],
      },
    ],
  },
];

export const ALL_TOPICS: TopicItem[] = SUBJECTS.flatMap((s) => s.topics);

export const getTopicById = (id: string): TopicItem | undefined => {
  return ALL_TOPICS.find((t) => t.id === id);
};

export const getSubjectById = (id: string): SubjectItem | undefined => {
  return SUBJECTS.find((s) => s.id === id);
};
