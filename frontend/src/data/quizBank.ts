export interface QuizQuestion {
  id: string; subject: string; topicId: string; text: string; options: string[]; correct: number; explanation: string;
}
type Row = [string, string, string[], number, string]; // topicId, text, options, correct, explanation

const build = (subject: string, rows: Row[]): QuizQuestion[] =>
  rows.map(([topicId, text, options, correct, explanation], i) => ({ id: `${subject}-${i}`, subject, topicId, text, options, correct, explanation }));

export const QUIZ_BANK: QuizQuestion[] = [
  ...build('python', [
    ['py-basics', 'Which Python data type is mutable?', ['Tuple', 'List', 'String', 'int'], 1, 'Lists can be changed in place; tuples, strings and ints cannot.'],
    ['py-basics', 'What does len([1, 2, 3]) return?', ['2', '3', '4', 'Error'], 1, 'len counts the items in the list.'],
    ['py-functions', 'What does a function return if it has no return statement?', ['0', 'False', 'None', 'An error'], 2, 'Python functions return None by default.'],
    ['py-recursion', 'What must every recursive function have?', ['A loop', 'A base case', 'A global variable', 'A class'], 1, 'The base case stops the recursion.'],
    ['py-recursion', 'What happens when recursion has no base case?', ['It returns None', 'RecursionError', 'It runs once', 'It pauses'], 1, 'The call stack overflows, raising RecursionError.'],
    ['py-dp', 'What does memoization do?', ['Compresses code', 'Caches results of repeated calls', 'Sorts data', 'Removes recursion'], 1, 'It stores results so repeated subproblems are not recomputed.'],
  ]),
  ...build('sql', [
    ['sql-basics', 'Which clause filters rows before grouping?', ['HAVING', 'WHERE', 'ORDER BY', 'LIMIT'], 1, 'WHERE filters rows; HAVING filters groups.'],
    ['sql-basics', 'What does SELECT DISTINCT do?', ['Sorts rows', 'Returns unique values', 'Deletes duplicates', 'Counts rows'], 1, 'It removes duplicate rows from the result.'],
    ['sql-joins', 'Which JOIN keeps all rows from the left table?', ['INNER JOIN', 'LEFT JOIN', 'CROSS JOIN', 'SELF JOIN'], 1, 'LEFT JOIN keeps unmatched left rows, filling NULLs.'],
    ['sql-aggregations', 'Which function counts rows?', ['SUM()', 'COUNT()', 'AVG()', 'TOTAL()'], 1, 'COUNT() returns the number of rows.'],
    ['sql-design', 'What does normalization reduce?', ['Query speed', 'Data redundancy', 'Table count', 'Security'], 1, 'Normalization removes duplicated data across tables.'],
    ['sql-design', 'A foreign key links a table to…', ['Any column', 'Another table’s primary key', 'An index', 'A view'], 1, 'It references the primary key of a related table.'],
  ]),
  ...build('statistics', [
    ['stats-basics', 'Which measure is most robust to outliers?', ['Mean', 'Median', 'Range', 'Variance'], 1, 'The median ignores extreme values.'],
    ['stats-basics', 'Standard deviation measures…', ['Central value', 'Spread of data', 'Sample size', 'Skew only'], 1, 'It describes how spread out values are around the mean.'],
    ['stats-probability', 'P(A and B) for independent events equals…', ['P(A)+P(B)', 'P(A)×P(B)', 'P(A)−P(B)', 'P(A)/P(B)'], 1, 'Independent probabilities multiply.'],
    ['stats-distributions', 'The Central Limit Theorem says sample means tend toward…', ['Uniform', 'Normal distribution', 'Binomial', 'Zero'], 1, 'With enough samples, means are approximately normal.'],
    ['stats-hypothesis', 'A small p-value suggests…', ['Strong evidence against the null', 'The null is true', 'A big effect always', 'Bad data'], 0, 'It means the data is unlikely under the null hypothesis.'],
    ['stats-hypothesis', 'A Type I error is…', ['Missing a real effect', 'Rejecting a true null', 'Wrong sample size', 'Using a t-test'], 1, 'A false positive: rejecting the null when it is true.'],
  ]),
  ...build('ml', [
    ['ml-foundations', 'Why split data into train and test sets?', ['Save memory', 'Measure generalisation', 'Speed training', 'Remove noise'], 1, 'The test set estimates performance on unseen data.'],
    ['ml-foundations', 'What is overfitting?', ['Model too simple', 'Model memorises training data', 'Too little data', 'Slow training'], 1, 'It fits noise in training data and fails to generalise.'],
    ['ml-supervised', 'Which task predicts a category?', ['Regression', 'Classification', 'Clustering', 'Dimensionality reduction'], 1, 'Classification predicts discrete labels.'],
    ['ml-unsupervised', 'K-means is an example of…', ['Classification', 'Clustering', 'Regression', 'Reinforcement'], 1, 'It groups unlabelled data into k clusters.'],
    ['ml-neural-nets', 'Backpropagation is used to…', ['Load data', 'Compute gradients to update weights', 'Pick features', 'Split data'], 1, 'It propagates error backwards to compute gradients.'],
    ['ml-neural-nets', 'What does an activation function add?', ['Memory', 'Non-linearity', 'More data', 'Regularisation only'], 1, 'Non-linearity lets networks model complex patterns.'],
  ]),
  ...build('dsa', [
    ['dsa-arrays', 'Time complexity of binary search?', ['O(n)', 'O(log n)', 'O(n²)', 'O(1)'], 1, 'It halves the search space each step.'],
    ['dsa-arrays', 'Two-pointer technique works best on…', ['Sorted arrays', 'Any graph', 'Hash maps', 'Trees only'], 0, 'Sorted order lets pointers move predictably.'],
    ['dsa-linked-lists', 'Which structure is last-in, first-out?', ['Queue', 'Stack', 'Heap', 'Graph'], 1, 'A stack pops the most recently pushed item.'],
    ['dsa-trees', 'In-order traversal of a BST returns values…', ['Random', 'Sorted ascending', 'Descending', 'By depth'], 1, 'Left, node, right visits a BST in sorted order.'],
    ['dsa-graphs', 'BFS uses which data structure?', ['Stack', 'Queue', 'Heap', 'Array only'], 1, 'A queue visits nodes level by level.'],
    ['dsa-graphs', 'Dijkstra’s algorithm finds…', ['Minimum spanning tree', 'Shortest paths (non-negative weights)', 'Cycles', 'Topological order'], 1, 'It finds shortest paths from a source with non-negative edges.'],
  ]),
];
