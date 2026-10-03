export interface AssessmentOption {
  text: string;
  weights: {
    visual?: number;
    auditory?: number;
    readWrite?: number;
    kinesthetic?: number;
    focusEndurance?: number;
    retention?: number;
    learningPace?: number;
    consistency?: number;
  };
}

export interface AssessmentQuestion {
  id: string;
  scenario: string;
  question?: string;
  category: string;
  options: AssessmentOption[];
}

export const ASSESSMENT_QUESTIONS: AssessmentQuestion[] = [
  {
    id: 'aq1',
    category: 'Information Input',
    scenario: 'You are tasked with understanding how an unfamiliar distributed system communicates across microservices.',
    question: 'What is your immediate first step to understand the architecture?',
    options: [
      {
        text: 'Look for an architectural flowchart, sequence diagram, or color-coded topology graph.',
        weights: { visual: 30, kinesthetic: 5, learningPace: 15 },
      },
      {
        text: 'Join a technical walkthrough call or listen to the lead architect explain the system orally.',
        weights: { auditory: 30, retention: 10 },
      },
      {
        text: 'Read the written engineering design document, API markdown specs, and RFC proposals.',
        weights: { readWrite: 30, focusEndurance: 15 },
      },
      {
        text: 'Clone the repo, set breakpoints in a debugger, and step through live request payloads hands-on.',
        weights: { kinesthetic: 30, learningPace: 20 },
      },
    ],
  },
  {
    id: 'aq2',
    category: 'Study Endurance & Focus',
    scenario: 'You have scheduled a 2-hour technical deep-dive block on Sunday morning.',
    question: 'How do you structure your focus session to absorb difficult algorithms?',
    options: [
      {
        text: 'Ultra-focused 25-minute Pomodoro sprints followed by structured 5-minute physical breaks.',
        weights: { focusEndurance: 20, consistency: 25, learningPace: 15 },
      },
      {
        text: 'Uninterrupted 90-to-120-minute flow state without looking at phone or notifications.',
        weights: { focusEndurance: 35, retention: 20 },
      },
      {
        text: 'Dynamic intervals: 45 minutes of theory followed immediately by 30 minutes of coding.',
        weights: { kinesthetic: 20, focusEndurance: 25, consistency: 15 },
      },
      {
        text: 'Fluid session switching between video lectures, sketches, and notes whenever focus wavers.',
        weights: { visual: 20, learningPace: 25, focusEndurance: 10 },
      },
    ],
  },
  {
    id: 'aq3',
    category: 'Problem-Solving Strategy',
    scenario: 'You encounter a tricky bug: `RecursionError: maximum recursion depth exceeded`.',
    question: 'How do you trace and solve the underlying issue?',
    options: [
      {
        text: 'Draw out the recursion tree on paper or whiteboard with branches, arguments, and return values.',
        weights: { visual: 30, retention: 15 },
      },
      {
        text: 'Talk through the base condition logic out loud using rubber-duck debugging.',
        weights: { auditory: 30, consistency: 10 },
      },
      {
        text: 'Carefully read stack trace line by line, inspect variable state tables, and write unit assertions.',
        weights: { readWrite: 25, focusEndurance: 20 },
      },
      {
        text: 'Insert print logs or interactive breakpoints inside the function and experiment with test inputs.',
        weights: { kinesthetic: 30, learningPace: 15 },
      },
    ],
  },
  {
    id: 'aq4',
    category: 'Memory & Long-term Retention',
    scenario: 'You learned dynamic programming concepts 3 weeks ago and need to recall memoization patterns today.',
    question: 'What helps you recall and apply those patterns most effortlessly?',
    options: [
      {
        text: 'Visualizing the grid tabulation matrix and color-highlighted state transitions in your mind.',
        weights: { visual: 30, retention: 25 },
      },
      {
        text: 'Recalling the mnemonic or rule-of-thumb phrasing you verbalized during study.',
        weights: { auditory: 25, retention: 20 },
      },
      {
        text: 'Consulting your own structured markdown notes and summary cheat-sheets.',
        weights: { readWrite: 30, consistency: 20, retention: 20 },
      },
      {
        text: 'Muscle memory from typing out similar solution templates on LeetCode.',
        weights: { kinesthetic: 30, retention: 25, learningPace: 10 },
      },
    ],
  },
  {
    id: 'aq5',
    category: 'Learning Velocity',
    scenario: 'You need to learn SQL window functions (`ROW_NUMBER`, `RANK`, `LEAD`) before an exam in 48 hours.',
    question: 'What is your rapid-learning strategy?',
    options: [
      {
        text: 'Watch high-speed animated visual explainers and infographic cheat sheets.',
        weights: { visual: 25, learningPace: 30 },
      },
      {
        text: 'Speed-run 15 interactive practice problems on an online query playground.',
        weights: { kinesthetic: 30, learningPace: 35 },
      },
      {
        text: 'Read official PostgreSQL documentation syntax sections and write concise summary notes.',
        weights: { readWrite: 25, focusEndurance: 20, learningPace: 15 },
      },
      {
        text: 'Listen to a comprehensive podcast or recorded lecture explaining use-cases.',
        weights: { auditory: 25, learningPace: 20 },
      },
    ],
  },
  {
    id: 'aq6',
    category: 'Study Habit & Consistency',
    scenario: 'Consider your learning rhythm over a typical month.',
    question: 'Which statement most accurately mirrors your daily schedule?',
    options: [
      {
        text: 'I study consistently at the exact same hour every day (e.g. 45 mins every morning).',
        weights: { consistency: 35, retention: 20, focusEndurance: 20 },
      },
      {
        text: 'I operate in high-intensity weekend bursts or hackathon-style marathon sessions.',
        weights: { learningPace: 30, focusEndurance: 25, consistency: 10 },
      },
      {
        text: 'I study daily but adapt duration flexibly depending on my energy levels and milestones.',
        weights: { consistency: 25, learningPace: 20 },
      },
      {
        text: 'I learn reactively whenever a project demand, curiosity, or assignment deadline arises.',
        weights: { learningPace: 25, kinesthetic: 20, consistency: 5 },
      },
    ],
  },
  {
    id: 'aq7',
    category: 'Concept Assimilation',
    scenario: 'You are studying Machine Learning Gradient Descent optimization.',
    question: 'How do you best grasp how the learning rate and derivative updates work?',
    options: [
      {
        text: 'An interactive 3D contour graph showing a ball rolling down the loss surface valley.',
        weights: { visual: 35, learningPace: 20 },
      },
      {
        text: 'An analogy of navigating down a foggy mountain slope explained conversationally.',
        weights: { auditory: 30, retention: 20 },
      },
      {
        text: 'Step-by-step mathematical proofs with partial derivative equations and notations.',
        weights: { readWrite: 35, focusEndurance: 25 },
      },
      {
        text: 'Writing a 20-line Python loop with NumPy from scratch and printing loss values.',
        weights: { kinesthetic: 35, learningPace: 20 },
      },
    ],
  },
  {
    id: 'aq8',
    category: 'Collaboration & Feedback',
    scenario: 'You are preparing for a group project presentation or coding defense.',
    question: 'How do you ensure you truly have mastered the material?',
    options: [
      {
        text: 'Explain the topic out loud to a peer or teammate until they understand it (Feynman technique).',
        weights: { auditory: 35, retention: 25 },
      },
      {
        text: 'Prepare a slide deck with clear diagrams, concept maps, and bullet summaries.',
        weights: { visual: 25, readWrite: 20 },
      },
      {
        text: 'Write a comprehensive reference guide or technical blog post covering edge cases.',
        weights: { readWrite: 35, retention: 20, consistency: 15 },
      },
      {
        text: 'Build a live working prototype or sandbox demo to prove the implementation.',
        weights: { kinesthetic: 35, learningPace: 20 },
      },
    ],
  },
  {
    id: 'aq9',
    category: 'Handling Distractions',
    scenario: 'You are reading a dense academic paper or documentation page and lose focus.',
    question: 'What is your best recovery mechanism?',
    options: [
      {
        text: 'Highlight key passages with colors, annotate margins, and sketch key concepts.',
        weights: { visual: 25, readWrite: 25, focusEndurance: 20 },
      },
      {
        text: 'Read the paragraphs out loud in a clear voice to force active mental engagement.',
        weights: { auditory: 35, focusEndurance: 20 },
      },
      {
        text: 'Switch immediately to implementing the algorithm in an IDE to see it work.',
        weights: { kinesthetic: 35, learningPace: 20 },
      },
      {
        text: 'Step away for a 3-minute stretch, sip water, and return with a timer running.',
        weights: { focusEndurance: 30, consistency: 25 },
      },
    ],
  },
  {
    id: 'aq10',
    category: 'Revision Technique',
    scenario: 'You have a comprehensive final quiz covering 5 topics in 3 days.',
    question: 'Which revision methodology do you trust most for peak exam performance?',
    options: [
      {
        text: 'Spaced repetition flashcards (Anki style) reviewed consistently every day.',
        weights: { consistency: 35, retention: 35 },
      },
      {
        text: 'Reviewing visual mind maps connecting all five subjects and their dependencies.',
        weights: { visual: 35, retention: 20 },
      },
      {
        text: 'Re-reading your textbook notes and writing one-page cheat sheets for each topic.',
        weights: { readWrite: 35, focusEndurance: 20 },
      },
      {
        text: 'Doing mock timed quizzes and coding problems without looking at solutions.',
        weights: { kinesthetic: 30, learningPace: 25, retention: 25 },
      },
    ],
  },
  {
    id: 'aq11',
    category: 'New Tool Adoption',
    scenario: 'A brand-new framework or library (e.g. FastAPI, Tailwind, PyTorch) is introduced in class.',
    question: 'How do you approach learning its syntax and best practices?',
    options: [
      {
        text: 'Watch a 20-minute video overview showing the UI, project structure, and component hierarchy.',
        weights: { visual: 30, learningPace: 20 },
      },
      {
        text: 'Read the official "Getting Started" guide from top to bottom before writing any code.',
        weights: { readWrite: 35, focusEndurance: 25 },
      },
      {
        text: 'Immediately run `npx create-...` or `pip install` and build a toy app by trial and error.',
        weights: { kinesthetic: 35, learningPace: 30 },
      },
      {
        text: 'Listen to tech podcasts, conference talks, or developer interviews discussing why it was created.',
        weights: { auditory: 30, retention: 15 },
      },
    ],
  },
  {
    id: 'aq12',
    category: 'Cognitive Processing Depth',
    scenario: 'When learning abstract concepts like Big-O algorithmic complexity:',
    question: 'What makes the concept "click" for you?',
    options: [
      {
        text: 'A comparison chart plotting execution time vs input size curves ($O(1), O(N), O(N^2), O(2^N)$).',
        weights: { visual: 35, retention: 20 },
      },
      {
        text: 'Counting iterations inside nested loops by stepping through with your fingers or pencil.',
        weights: { kinesthetic: 30, focusEndurance: 20 },
      },
      {
        text: 'Precise formal definitions with upper and lower bounding equations ($f(n) \\le c \\cdot g(n)$).',
        weights: { readWrite: 35, focusEndurance: 25 },
      },
      {
        text: 'An intuitive verbal analogy (e.g. searching a phonebook page by page vs ripping it in half).',
        weights: { auditory: 30, learningPace: 20 },
      },
    ],
  },
  {
    id: 'aq13',
    category: 'Energy & Fatigue Resistance',
    scenario: 'It is 9:00 PM and you have been studying for 4 hours.',
    question: 'How does your brain respond to continuous cognitive load?',
    options: [
      {
        text: 'My retention drops sharply; I need to switch off and sleep to consolidate memory.',
        weights: { retention: 15, consistency: 25 },
      },
      {
        text: 'I can maintain high analytical focus if I have quiet music, coffee, or isolated silence.',
        weights: { focusEndurance: 35, retention: 25 },
      },
      {
        text: 'I can keep going if I switch from reading theory to engaging hands-on coding puzzles.',
        weights: { kinesthetic: 30, focusEndurance: 25, learningPace: 20 },
      },
      {
        text: 'I absorb things quickly early in the block, but my speed tapers off over time.',
        weights: { learningPace: 30, focusEndurance: 15 },
      },
    ],
  },
  {
    id: 'aq14',
    category: 'Information Structuring',
    scenario: 'You are organizing your semester course notes in Notion, Obsidian, or a notebook.',
    question: 'What is your note-taking philosophy?',
    options: [
      {
        text: 'Heavily visual: Canvas boards, embedded diagrams, color badges, and mind-map nodes.',
        weights: { visual: 35, consistency: 15 },
      },
      {
        text: 'Extensive hierarchical bullet points, formatted code blocks, and glossary definitions.',
        weights: { readWrite: 35, consistency: 25, retention: 20 },
      },
      {
        text: 'Voice memos, lecture recordings, and transcription highlights.',
        weights: { auditory: 35, retention: 15 },
      },
      {
        text: 'Minimal written notes—mostly executable Jupyter notebooks and Git commits.',
        weights: { kinesthetic: 35, learningPace: 25 },
      },
    ],
  },
  {
    id: 'aq15',
    category: 'Error Analysis & Debugging',
    scenario: 'You receive a 60% on a practice test on SQL Joins.',
    question: 'How do you analyze your incorrect answers?',
    options: [
      {
        text: 'Create a Venn diagram of table intersections to visually see where the logic failed.',
        weights: { visual: 35, retention: 20 },
      },
      {
        text: 'Re-run the exact failing queries on a local SQLite database and inspect output tables.',
        weights: { kinesthetic: 35, learningPace: 20 },
      },
      {
        text: 'Write out the full explanation in your study journal describing why the right answer is correct.',
        weights: { readWrite: 30, consistency: 25, retention: 25 },
      },
      {
        text: 'Discuss the missed questions with a tutor or study buddy to hear their mental model.',
        weights: { auditory: 30, retention: 20 },
      },
    ],
  },
  {
    id: 'aq16',
    category: 'Pacing & Deadline Pressure',
    scenario: 'You are given a two-week window to finish a major Machine Learning project.',
    question: 'How do you pace your execution across the 14 days?',
    options: [
      {
        text: 'Break it into 14 equal daily 45-minute milestones and track progress on a kanban board.',
        weights: { consistency: 40, focusEndurance: 25 },
      },
      {
        text: 'Sprint rapidly through 80% of the project in the first 3 days, then iterate slowly on polish.',
        weights: { learningPace: 35, kinesthetic: 20 },
      },
      {
        text: 'Spend the first week reading literature and planning architecture before writing any code.',
        weights: { readWrite: 30, focusEndurance: 30, retention: 25 },
      },
      {
        text: 'Form a study group to meet every 3 days to debate design decisions and review progress.',
        weights: { auditory: 30, consistency: 20 },
      },
    ],
  },
  {
    id: 'aq17',
    category: 'Learning Environment',
    scenario: 'What is your ideal physical and auditory setup for maximum comprehension?',
    options: [
      {
        text: 'A clean desk with multiple monitors displaying visual diagrams, code, and documentation.',
        weights: { visual: 30, focusEndurance: 20 },
      },
      {
        text: 'Noise-cancelling headphones playing binaural beats, lo-fi beats, or ambient café noise.',
        weights: { auditory: 30, focusEndurance: 25 },
      },
      {
        text: 'Total library silence with physical notebook, highlighters, and reference textbooks.',
        weights: { readWrite: 35, focusEndurance: 30 },
      },
      {
        text: 'A standing desk with a mechanical keyboard where you can pace around and fidget while thinking.',
        weights: { kinesthetic: 35, learningPace: 20 },
      },
    ],
  },
  {
    id: 'aq18',
    category: 'Confidence Building',
    scenario: 'When stepping into a complex topic like Neural Networks for the first time:',
    question: 'What gives you the highest confidence that you are on the right track?',
    options: [
      {
        text: 'Being able to draw the entire computational graph with forward and backward loss arrows.',
        weights: { visual: 35, retention: 20 },
      },
      {
        text: 'Training a model that reaches 95% accuracy on a validation dataset.',
        weights: { kinesthetic: 35, learningPace: 25 },
      },
      {
        text: 'Being able to write a clear 2-page essay explaining the math without consulting reference notes.',
        weights: { readWrite: 35, focusEndurance: 25, retention: 25 },
      },
      {
        text: 'Successfully explaining gradient backpropagation to a classmate without stumbling.',
        weights: { auditory: 35, retention: 25 },
      },
    ],
  },
  {
    id: 'aq19',
    category: 'Motivation & Goal Tracking',
    scenario: 'What kind of progress metric keeps you most motivated across a semester?',
    options: [
      {
        text: 'Maintaining an unbroken 30-day streak on your learning dashboard.',
        weights: { consistency: 40, retention: 20 },
      },
      {
        text: 'Watching your mastery radar chart expand and unlocking new visual skill badges.',
        weights: { visual: 30, learningPace: 25 },
      },
      {
        text: 'Seeing your portfolio of shipped projects and real-world GitHub repositories grow.',
        weights: { kinesthetic: 35, learningPace: 25 },
      },
      {
        text: 'Scoring in the top 10% on technical assessments and receiving detailed written feedback.',
        weights: { readWrite: 30, focusEndurance: 25 },
      },
    ],
  },
  {
    id: 'aq20',
    category: 'Metacognition & Synthesis',
    scenario: 'You want to consolidate everything you learned this month before starting a new domain.',
    question: 'What is your capstone consolidation activity?',
    options: [
      {
        text: 'Build a comprehensive master mind-map connecting Python, SQL, Statistics, ML, and DSA.',
        weights: { visual: 35, retention: 30 },
      },
      {
        text: 'Record a 10-minute video/podcast walkthrough explaining the semester’s core breakthroughs.',
        weights: { auditory: 35, retention: 25 },
      },
      {
        text: 'Publish a polished technical cheat-sheet and documentation guide for other students.',
        weights: { readWrite: 35, consistency: 25, retention: 25 },
      },
      {
        text: 'Build an end-to-end full-stack data science app that combines databases, models, and code.',
        weights: { kinesthetic: 35, learningPace: 30 },
      },
    ],
  },
];
