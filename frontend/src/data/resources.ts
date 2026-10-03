import type { Modality } from '../utils/dnaEngine';

export interface Resource { id: number; title: string; url: string; subject: string; type: string; style: Modality }

export const RESOURCES: Resource[] = [
  { id: 1, title: 'Python Tutor: visualise code execution', url: 'https://pythontutor.com/', subject: 'python', type: 'Interactive', style: 'visual' },
  { id: 2, title: 'Official Python Tutorial', url: 'https://docs.python.org/3/tutorial/', subject: 'python', type: 'Documentation', style: 'readWrite' },
  { id: 3, title: 'Real Python: Recursion in Python', url: 'https://realpython.com/python-recursion/', subject: 'python', type: 'Article', style: 'readWrite' },
  { id: 4, title: 'Exercism Python Track', url: 'https://exercism.org/tracks/python', subject: 'python', type: 'Practice', style: 'kinesthetic' },
  { id: 5, title: 'SQLBolt: interactive SQL lessons', url: 'https://sqlbolt.com/', subject: 'sql', type: 'Interactive', style: 'kinesthetic' },
  { id: 6, title: 'SQL Murder Mystery', url: 'https://mystery.knightlab.com/', subject: 'sql', type: 'Practice', style: 'kinesthetic' },
  { id: 7, title: 'Visual Guide to SQL Joins', url: 'https://www.atlassian.com/data/sql/sql-join-types-explained-visually', subject: 'sql', type: 'Article', style: 'visual' },
  { id: 8, title: 'StatQuest with Josh Starmer', url: 'https://www.youtube.com/@statquest', subject: 'statistics', type: 'Video', style: 'auditory' },
  { id: 9, title: 'Seeing Theory: visual probability', url: 'https://seeing-theory.brown.edu/', subject: 'statistics', type: 'Interactive', style: 'visual' },
  { id: 10, title: 'Khan Academy Statistics', url: 'https://www.khanacademy.org/math/statistics-probability', subject: 'statistics', type: 'Course', style: 'auditory' },
  { id: 11, title: '3Blue1Brown: Neural Networks', url: 'https://www.youtube.com/@3blue1brown', subject: 'ml', type: 'Video', style: 'visual' },
  { id: 12, title: 'scikit-learn User Guide', url: 'https://scikit-learn.org/stable/user_guide.html', subject: 'ml', type: 'Documentation', style: 'readWrite' },
  { id: 13, title: 'Google ML Crash Course', url: 'https://developers.google.com/machine-learning/crash-course', subject: 'ml', type: 'Course', style: 'kinesthetic' },
  { id: 14, title: 'VisuAlgo: animated algorithms', url: 'https://visualgo.net/', subject: 'dsa', type: 'Interactive', style: 'visual' },
  { id: 15, title: 'NeetCode: explained problem walkthroughs', url: 'https://neetcode.io/', subject: 'dsa', type: 'Video', style: 'auditory' },
  { id: 16, title: 'CS50 lectures', url: 'https://cs50.harvard.edu/x/', subject: 'dsa', type: 'Course', style: 'auditory' },
  { id: 17, title: 'LeetCode practice problems', url: 'https://leetcode.com/problemset/', subject: 'dsa', type: 'Practice', style: 'kinesthetic' },
];
