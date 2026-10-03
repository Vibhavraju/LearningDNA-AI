import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import Dashboard from './pages/Dashboard';
import AssessmentPage from './pages/Assessment';
import MyLearningDNA from './pages/MyLearningDNA';
import StudyPlan from './pages/StudyPlan';
import QuizRunner from './pages/QuizRunner';
import AITutor from './pages/AITutor';
import Resources from './pages/Resources';
import Settings from './pages/Settings';
import { useUserStore } from './store/userStore';

export default function App() {
  const { isOnboardingComplete, dnaProfile, userProfile } = useUserStore();
  if (!isOnboardingComplete || !dnaProfile || !userProfile?.name) return <AssessmentPage />;

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dna" element={<MyLearningDNA />} />
          <Route path="/plan" element={<StudyPlan />} />
          <Route path="/quiz" element={<QuizRunner />} />
          <Route path="/tutor" element={<AITutor />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}
