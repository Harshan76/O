import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams, useNavigate, Link } from 'react-router-dom';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { CourseLearningHubData, CourseTopicResource, StudentNote } from '../types';
import { 
  BookOpen, Video, Edit3, Brain, Play, CheckCircle2, 
  Clock, ExternalLink, Search, Trash2, Edit, Plus, 
  ChevronRight, ArrowLeft, ArrowRight, Lightbulb, AlertCircle, Eye, EyeOff,
  Printer, FileText, Download, Check
} from 'lucide-react';

export const CourseLearningHubPage: React.FC = () => {
  const { courseId: paramCourseId } = useParams<{ courseId?: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { showToast, learner } = useLearner();

  const activeCourseId = paramCourseId || searchParams.get('courseId') || 'c-python';

  const [loading, setLoading] = useState(true);
  const [hubData, setHubData] = useState<CourseLearningHubData | null>(null);
  const [selectedTopicId, setSelectedTopicId] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'notes' | 'videos' | 'smart_notes' | 'pdf'>('notes');

  // Personal Smart Notes state
  const [notes, setNotes] = useState<StudentNote[]>([]);
  const [loadingNotes, setLoadingNotes] = useState(false);
  const [isEditingNote, setIsEditingNote] = useState(false);
  const [editingNoteId, setEditingNoteId] = useState<string | null>(null);
  const [noteTitle, setNoteTitle] = useState('');
  const [noteContent, setNoteContent] = useState('');
  const [noteTopicId, setNoteTopicId] = useState('');
  const [noteToDelete, setNoteToDelete] = useState<StudentNote | null>(null);
  const [topicFilter, setTopicFilter] = useState<string>('all');

  // Practice questions revealed toggle state
  const [revealedAnswers, setRevealedAnswers] = useState<Record<number, boolean>>({});

  const availableCourses = [
    { id: 'c-python', title: 'Python Programming', domain: 'Software Dev' },
    { id: 'c-fullstack', title: 'Full-Stack Web Architecture', domain: 'Web Dev' },
    { id: 'c-datasci', title: 'Data Science & ML', domain: 'Data Science' },
    { id: 'c-ai-eng', title: 'AI Engineering & LLMs', domain: 'AI Systems' }
  ];

  // Fetch course resources
  const fetchHubData = async (courseId: string) => {
    try {
      setLoading(true);
      const data = await api.getCourseResources(courseId);
      setHubData(data);
      if (data.topics && data.topics.length > 0) {
        const queryTopic = searchParams.get('topic');
        const matched = data.topics.find(t => t.id === queryTopic);
        if (matched) {
          setSelectedTopicId(matched.id);
        } else {
          setSelectedTopicId(data.topics[0].id);
        }
      }
      const queryTab = searchParams.get('tab') as 'notes' | 'videos' | 'smart_notes' | 'pdf' | null;
      if (queryTab && ['notes', 'videos', 'smart_notes', 'pdf'].includes(queryTab)) {
        setActiveTab(queryTab);
      }
    } catch (err: any) {
      showToast(err.message || 'Failed to load course resources', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Fetch student smart notes
  const fetchNotes = async (courseId: string) => {
    try {
      setLoadingNotes(true);
      const studentNotes = await api.getCourseNotes(courseId);
      setNotes(studentNotes);
    } catch (err: any) {
      console.warn('Could not fetch notes from server:', err);
    } finally {
      setLoadingNotes(false);
    }
  };

  useEffect(() => {
    fetchHubData(activeCourseId);
    fetchNotes(activeCourseId);
    setIsEditingNote(false);
    setRevealedAnswers({});
  }, [activeCourseId]);

  // Synchronize when search query params change
  useEffect(() => {
    const queryTopic = searchParams.get('topic');
    if (queryTopic && hubData?.topics?.some(t => t.id === queryTopic)) {
      setSelectedTopicId(queryTopic);
    }
    const queryTab = searchParams.get('tab') as 'notes' | 'videos' | 'smart_notes' | 'pdf' | null;
    if (queryTab && ['notes', 'videos', 'smart_notes', 'pdf'].includes(queryTab)) {
      setActiveTab(queryTab);
    }
  }, [searchParams, hubData]);

  const activeTopic = hubData?.topics?.find(t => t.id === selectedTopicId) || hubData?.topics?.[0];

  const handleSwitchCourse = (newCourseId: string) => {
    navigate(`/courses/${newCourseId}/learn`);
  };

  const handleStartCreateNote = () => {
    setEditingNoteId(null);
    setNoteTitle('');
    setNoteContent('');
    setNoteTopicId(activeTopic?.id || '');
    setIsEditingNote(true);
  };

  const handleStartEditNote = (note: StudentNote) => {
    setEditingNoteId(note.id);
    setNoteTitle(note.title);
    setNoteContent(note.content);
    setNoteTopicId(note.topic_id || activeTopic?.id || '');
    setIsEditingNote(true);
  };

  const handleCancelNote = () => {
    setIsEditingNote(false);
    setEditingNoteId(null);
    setNoteTitle('');
    setNoteContent('');
  };

  const handleSaveNote = async () => {
    if (!noteTitle.trim()) {
      showToast('Please enter a note title.', 'warning');
      return;
    }
    if (!noteContent.trim()) {
      showToast('Please enter note content.', 'warning');
      return;
    }

    const topicObj = hubData?.topics?.find(t => t.id === noteTopicId);
    const topicTitle = topicObj ? topicObj.title : (activeTopic?.title || 'General');

    try {
      if (editingNoteId) {
        await api.updateCourseNote(activeCourseId, editingNoteId, {
          title: noteTitle.trim(),
          content: noteContent.trim(),
          topic_id: noteTopicId,
          topic_title: topicTitle
        });
        showToast('Smart note updated successfully.', 'success');
      } else {
        await api.createCourseNote(activeCourseId, {
          title: noteTitle.trim(),
          content: noteContent.trim(),
          topic_id: noteTopicId,
          topic_title: topicTitle
        });
        showToast('Smart note saved successfully.', 'success');
      }
      handleCancelNote();
      await fetchNotes(activeCourseId);
    } catch (err: any) {
      showToast(err.message || 'Failed to save note', 'error');
    }
  };

  const handleDeleteNoteConfirm = async () => {
    if (!noteToDelete) return;
    try {
      await api.deleteCourseNote(activeCourseId, noteToDelete.id);
      showToast('Note deleted successfully.', 'info');
      setNoteToDelete(null);
      await fetchNotes(activeCourseId);
    } catch (err: any) {
      showToast(err.message || 'Failed to delete note', 'error');
    }
  };

  const toggleAnswerReveal = (index: number) => {
    setRevealedAnswers(prev => ({ ...prev, [index]: !prev[index] }));
  };

  // Filtered notes for the smart notes tab
  const filteredNotes = notes.filter(n => {
    if (topicFilter === 'all') return true;
    return n.topic_id === topicFilter;
  });

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      {/* Navigation Breadcrumb */}
      <div className="flex items-center justify-between gap-4">
        <Link
          to="/goals-courses"
          className="inline-flex items-center gap-1.5 text-xs font-bold font-mono text-zinc-700 hover:text-black transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to All Courses</span>
        </Link>
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono font-bold text-zinc-500 uppercase">Switch Track:</span>
          <select
            value={activeCourseId}
            onChange={(e) => handleSwitchCourse(e.target.value)}
            className="bg-white text-xs font-mono font-bold text-black border-2 border-black rounded-lg px-2.5 py-1 shadow-neo-xs focus:outline-none"
          >
            {availableCourses.map((c) => (
              <option key={c.id} value={c.id}>{c.title}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Course Learning Hub Header Card */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold bg-[#FEF08A] px-2.5 py-0.5 rounded border border-black">
                {hubData?.domain || 'Computer Science'}
              </span>
              <span className="text-xs font-mono font-bold bg-[#DDD6FE] px-2.5 py-0.5 rounded border border-black">
                {hubData?.level || 'Core'}
              </span>
              <span className="text-xs font-mono font-bold bg-black text-white px-2 py-0.5 rounded">
                Course Learning Hub
              </span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-black">
              {hubData?.course_title || 'Course Learning Hub'}
            </h1>
          </div>

          {/* Primary Learning-to-Test CTA Button */}
          <Link
            to={`/diagnostic?courseId=${activeCourseId}`}
            className="bg-[#A7F3D0] hover:bg-[#86efac] text-emerald-950 font-extrabold px-6 py-3 rounded-xl border-3 border-black shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-sm flex items-center gap-2.5 shrink-0"
          >
            <Brain className="w-5 h-5 text-emerald-900" />
            <span>Attempt Test</span>
            <ArrowRight className="w-4 h-4 text-emerald-900" />
          </Link>
        </div>

        <p className="text-sm text-zinc-700 font-medium max-w-4xl leading-relaxed">
          {hubData?.description}
        </p>

        {/* Learning Flow Steps Indicator */}
        <div className="border-t-2 border-black pt-4 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
          <div className="bg-zinc-50 border border-black rounded-lg p-2 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-[#FEF08A] border border-black flex items-center justify-center font-bold text-[10px]">1</span>
            <span className="font-bold text-zinc-800 truncate">Select Topic</span>
          </div>
          <div className="bg-zinc-50 border border-black rounded-lg p-2 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-[#DDD6FE] border border-black flex items-center justify-center font-bold text-[10px]">2</span>
            <span className="font-bold text-zinc-800 truncate">Study Notes</span>
          </div>
          <div className="bg-zinc-50 border border-black rounded-lg p-2 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-[#BAE6FD] border border-black flex items-center justify-center font-bold text-[10px]">3</span>
            <span className="font-bold text-zinc-800 truncate">Watch Videos</span>
          </div>
          <div className="bg-zinc-50 border border-black rounded-lg p-2 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-[#A7F3D0] border border-black flex items-center justify-center font-bold text-[10px]">4</span>
            <span className="font-bold text-zinc-800 truncate">Attempt Test</span>
          </div>
        </div>
      </div>

      {/* Topic Switcher Bar */}
      <div className="space-y-2">
        <div className="text-xs font-mono font-bold uppercase text-zinc-500 tracking-wider">
          Curriculum Topics ({hubData?.topics?.length || 0})
        </div>
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
          {hubData?.topics?.map((topic, idx) => (
            <button
              key={topic.id}
              onClick={() => setSelectedTopicId(topic.id)}
              className={`shrink-0 text-left p-3 rounded-xl border-2 transition-all flex items-center gap-2.5 text-xs font-bold ${
                selectedTopicId === topic.id
                  ? 'bg-[#FEF08A] border-black shadow-neo-sm text-black'
                  : 'bg-white border-black hover:bg-zinc-50 text-zinc-800'
              }`}
            >
              <span className="w-5 h-5 rounded-full bg-black text-white flex items-center justify-center text-[10px] font-mono shrink-0">
                {idx + 1}
              </span>
              <span className="font-extrabold truncate max-w-[200px]">{topic.title}</span>
              <span className="text-[10px] font-mono text-zinc-600 flex items-center gap-0.5 ml-1">
                <Clock className="w-3 h-3" />
                {topic.estimated_minutes}m
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Learning Hub Split Tabs */}
      <div className="space-y-6">
        {/* Navigation Tabs */}
        <div className="flex flex-wrap items-center gap-2 sm:gap-3 border-b-2 border-black pb-3">
          <button
            onClick={() => setActiveTab('notes')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold border-2 transition-all flex items-center gap-2 ${
              activeTab === 'notes'
                ? 'bg-black text-[#FEF08A] border-black shadow-neo-xs'
                : 'bg-white text-zinc-700 border-black hover:bg-zinc-100'
            }`}
          >
            <BookOpen className="w-4 h-4" />
            <span>Topic Study Notes</span>
          </button>

          <button
            onClick={() => setActiveTab('videos')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold border-2 transition-all flex items-center gap-2 ${
              activeTab === 'videos'
                ? 'bg-black text-[#FEF08A] border-black shadow-neo-xs'
                : 'bg-white text-zinc-700 border-black hover:bg-zinc-100'
            }`}
          >
            <Video className="w-4 h-4" />
            <span>Educational Videos ({activeTopic?.videos?.length || 0})</span>
          </button>

          <button
            onClick={() => setActiveTab('pdf')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold border-2 transition-all flex items-center gap-2 ${
              activeTab === 'pdf'
                ? 'bg-black text-[#FEF08A] border-black shadow-neo-xs'
                : 'bg-white text-zinc-700 border-black hover:bg-zinc-100'
            }`}
          >
            <Printer className="w-4 h-4" />
            <span>Study Guide & PDF</span>
          </button>

          <button
            onClick={() => setActiveTab('smart_notes')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-extrabold border-2 transition-all flex items-center gap-2 ${
              activeTab === 'smart_notes'
                ? 'bg-black text-[#FEF08A] border-black shadow-neo-xs'
                : 'bg-white text-zinc-700 border-black hover:bg-zinc-100'
            }`}
          >
            <Edit3 className="w-4 h-4" />
            <span>Smart Notes ({notes.length})</span>
          </button>
        </div>

        {/* TAB 1: TOPIC STUDY NOTES */}
        {activeTab === 'notes' && activeTopic && (
          <div className="space-y-6">
            {/* Topic Header & Introduction */}
            <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold bg-[#DDD6FE] px-2 py-0.5 rounded border border-black">
                    Topic Guide
                  </span>
                  <span className="text-xs font-mono text-zinc-600 flex items-center gap-1 font-bold">
                    <Clock className="w-3.5 h-3.5" />
                    Est. Time: {activeTopic.estimated_minutes} mins
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setActiveTab('videos')}
                    className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold px-3 py-1.5 rounded-lg border border-black shadow-neo-xs text-xs flex items-center gap-1.5 transition-all"
                  >
                    <Video className="w-3.5 h-3.5" />
                    <span>Watch Video</span>
                  </button>
                  <button
                    onClick={() => setActiveTab('pdf')}
                    className="bg-[#A7F3D0] hover:bg-[#86efac] text-emerald-950 font-extrabold px-3 py-1.5 rounded-lg border border-black shadow-neo-xs text-xs flex items-center gap-1.5 transition-all"
                  >
                    <Printer className="w-3.5 h-3.5" />
                    <span>Print / Save PDF</span>
                  </button>
                </div>
              </div>
              <h2 className="text-2xl font-extrabold text-black">{activeTopic.title}</h2>
              <p className="text-sm text-zinc-700 font-medium leading-relaxed bg-[#FAF7F2] p-4 rounded-xl border border-black">
                {activeTopic.study_notes.introduction}
              </p>
            </div>

            {/* Concepts and Definitions */}
            {activeTopic.study_notes.concepts?.length > 0 && (
              <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo space-y-4">
                <h3 className="text-lg font-extrabold text-black flex items-center gap-2">
                  <Lightbulb className="w-5 h-5 text-amber-500" />
                  <span>Important Concepts & Definitions</span>
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {activeTopic.study_notes.concepts.map((concept, i) => (
                    <div key={i} className="bg-zinc-50 border-2 border-black rounded-xl p-4 shadow-neo-xs space-y-1.5">
                      <div className="font-extrabold text-sm text-black flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                        {concept.term}
                      </div>
                      <p className="text-xs text-zinc-700 font-medium leading-relaxed">
                        {concept.definition}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Step-by-Step Explanations */}
            {activeTopic.study_notes.step_by_step?.length > 0 && (
              <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo space-y-4">
                <h3 className="text-lg font-extrabold text-black flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                  <span>Step-by-Step Methodology</span>
                </h3>
                <div className="space-y-3">
                  {activeTopic.study_notes.step_by_step.map((step) => (
                    <div key={step.step} className="flex items-start gap-3 p-3.5 bg-zinc-50 border border-black rounded-xl">
                      <div className="w-7 h-7 rounded-lg bg-black text-[#FEF08A] font-mono font-bold flex items-center justify-center shrink-0 text-xs">
                        {step.step}
                      </div>
                      <div className="space-y-0.5">
                        <h4 className="font-extrabold text-sm text-black">{step.title}</h4>
                        <p className="text-xs text-zinc-700 font-medium leading-relaxed">{step.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Code / Architecture Example */}
            {activeTopic.study_notes.code_example && (
              <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo space-y-4">
                <h3 className="text-lg font-extrabold text-black">Worked Example & Architecture</h3>
                <div className="bg-zinc-950 text-emerald-400 font-mono text-xs sm:text-sm p-5 rounded-xl border-2 border-black overflow-x-auto leading-relaxed shadow-neo-sm">
                  <pre>{activeTopic.study_notes.code_example.code}</pre>
                </div>
                <div className="bg-[#FAF7F2] border border-black rounded-xl p-3.5 text-xs text-zinc-800 font-medium leading-relaxed">
                  <strong>Explanation:</strong> {activeTopic.study_notes.code_example.explanation}
                </div>
              </div>
            )}

            {/* Key Takeaways */}
            {activeTopic.study_notes.key_takeaways?.length > 0 && (
              <div className="bg-[#FEF08A] border-3 border-black rounded-2xl p-6 shadow-neo space-y-3">
                <h3 className="text-base font-extrabold text-black uppercase tracking-wider font-mono">
                  Key Takeaways
                </h3>
                <ul className="space-y-2">
                  {activeTopic.study_notes.key_takeaways.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs sm:text-sm font-medium text-black">
                      <span className="font-bold text-base leading-none">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Practice Questions */}
            {activeTopic.study_notes.practice_questions?.length > 0 && (
              <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo space-y-4">
                <h3 className="text-lg font-extrabold text-black">Self-Check Practice Questions</h3>
                <div className="space-y-4">
                  {activeTopic.study_notes.practice_questions.map((pq, idx) => (
                    <div key={idx} className="bg-zinc-50 border-2 border-black rounded-xl p-4 space-y-3">
                      <div className="font-bold text-sm text-black flex items-start gap-2">
                        <span className="w-5 h-5 rounded-full bg-black text-white font-mono text-xs flex items-center justify-center shrink-0">
                          {idx + 1}
                        </span>
                        <span>{pq.question}</span>
                      </div>

                      <button
                        onClick={() => toggleAnswerReveal(idx)}
                        className="text-xs font-mono font-bold bg-white hover:bg-zinc-100 border border-black rounded-lg px-3 py-1 flex items-center gap-1.5 shadow-neo-xs transition-all"
                      >
                        {revealedAnswers[idx] ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                        <span>{revealedAnswers[idx] ? 'Hide Answer' : 'Reveal Answer & Explanation'}</span>
                      </button>

                      {revealedAnswers[idx] && (
                        <div className="bg-[#A7F3D0] border border-black rounded-lg p-3 text-xs font-medium text-emerald-950 space-y-1">
                          <div><strong>Answer:</strong> {pq.answer}</div>
                          <div><strong>Explanation:</strong> {pq.explanation}</div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
            {/* Bottom Quick-Action Banner on Notes */}
            <div className="bg-[#FAF7F2] border-2 border-black rounded-xl p-4 flex flex-wrap items-center justify-between gap-3 shadow-neo-xs">
              <div className="space-y-0.5">
                <span className="font-extrabold text-xs text-black">Ready for media walkthrough or offline study?</span>
                <p className="text-[11px] text-zinc-600 font-medium">Watch the curated video walkthrough or export this topic as a printable PDF guide.</p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setActiveTab('videos')}
                  className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold px-3 py-1.5 rounded-lg border border-black shadow-neo-xs text-xs flex items-center gap-1.5 transition-all"
                >
                  <Video className="w-3.5 h-3.5" />
                  <span>Watch Video ({activeTopic.videos?.length || 0})</span>
                </button>
                <button
                  onClick={() => setActiveTab('pdf')}
                  className="bg-[#A7F3D0] hover:bg-[#86efac] text-emerald-950 font-extrabold px-3 py-1.5 rounded-lg border border-black shadow-neo-xs text-xs flex items-center gap-1.5 transition-all"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>Open PDF Guide</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: EDUCATIONAL VIDEOS */}
        {activeTab === 'videos' && activeTopic && (
          <div className="space-y-6">
            <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold bg-[#BAE6FD] px-2 py-0.5 rounded border border-black">
                    Video Lecture Library
                  </span>
                  <span className="text-xs font-mono font-bold text-zinc-500">
                    Topic: {activeTopic.title}
                  </span>
                </div>
                <h2 className="text-2xl font-extrabold text-black">Educational Video Walkthroughs</h2>
                <p className="text-xs sm:text-sm text-zinc-600 font-medium">
                  Curated educational video lessons from trusted academic and industry creators for {activeTopic.title}.
                </p>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => setActiveTab('notes')}
                  className="bg-white hover:bg-zinc-100 text-black font-extrabold px-3 py-2 rounded-xl border-2 border-black shadow-neo-xs text-xs flex items-center gap-1.5 transition-all"
                >
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>Topic Notes</span>
                </button>
                <button
                  onClick={() => setActiveTab('pdf')}
                  className="bg-[#A7F3D0] hover:bg-[#86efac] text-emerald-950 font-extrabold px-3 py-2 rounded-xl border-2 border-black shadow-neo-xs text-xs flex items-center gap-1.5 transition-all"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>Printable PDF Guide</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {activeTopic.videos?.map((vid) => (
                <div
                  key={vid.id}
                  className="bg-white border-3 border-black rounded-2xl overflow-hidden shadow-neo flex flex-col justify-between"
                >
                  <div>
                    {/* Embedded Video Player */}
                    <div className="relative aspect-video w-full bg-black border-b-2 border-black">
                      <iframe
                        src={vid.embed_url}
                        title={vid.title}
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                        className="w-full h-full border-0"
                      />
                    </div>

                    {/* Video Metadata */}
                    <div className="p-5 space-y-3">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="font-bold bg-[#FEF08A] px-2 py-0.5 rounded border border-black">
                          {vid.channel}
                        </span>
                        <span className="text-zinc-600 font-bold flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5" />
                          {vid.duration}
                        </span>
                      </div>

                      <h3 className="font-extrabold text-base text-black leading-snug">
                        {vid.title}
                      </h3>

                      <p className="text-xs text-zinc-700 font-medium leading-relaxed">
                        {vid.summary}
                      </p>
                    </div>
                  </div>

                  {/* Fallback Direct Link, Search Link, and PDF Link */}
                  <div className="p-5 pt-0 border-t border-zinc-200 mt-2 flex flex-wrap items-center gap-2">
                    <a
                      href={vid.watch_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-[#FEF08A] hover:bg-[#fde047] text-black text-xs font-extrabold px-3 py-2 rounded-lg border border-black shadow-neo-xs flex items-center gap-1.5 transition-all"
                    >
                      <Play className="w-3.5 h-3.5 fill-black" />
                      <span>Watch on YouTube</span>
                      <ExternalLink className="w-3 h-3 ml-0.5" />
                    </a>

                    <button
                      onClick={() => setActiveTab('pdf')}
                      className="bg-[#A7F3D0] hover:bg-[#86efac] text-emerald-950 text-xs font-extrabold px-3 py-2 rounded-lg border border-black shadow-neo-xs flex items-center gap-1.5 transition-all"
                    >
                      <FileText className="w-3.5 h-3.5" />
                      <span>Topic PDF Guide</span>
                    </button>

                    <a
                      href={vid.search_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-zinc-100 hover:bg-zinc-200 text-zinc-800 text-xs font-bold px-3 py-2 rounded-lg border border-black flex items-center gap-1.5 transition-all"
                    >
                      <Search className="w-3.5 h-3.5" />
                      <span>More Tutorials</span>
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: PRINTABLE STUDY GUIDE & PDF */}
        {activeTab === 'pdf' && activeTopic && (
          <div className="space-y-6">
            {/* Top Action Toolbar (Hidden during print) */}
            <div className="no-print bg-white border-3 border-black rounded-2xl p-6 shadow-neo flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold bg-[#A7F3D0] px-2.5 py-0.5 rounded border border-black text-emerald-950">
                    Printable Study Guide
                  </span>
                  <span className="text-xs font-mono font-bold text-zinc-500">
                    Module ID: {activeTopic.id}
                  </span>
                </div>
                <h2 className="text-2xl font-extrabold text-black">
                  {activeTopic.title} • Study Guide & PDF
                </h2>
                <p className="text-xs sm:text-sm text-zinc-600 font-medium">
                  Technical notes, core definitions, code blueprint, and practice questions formatted for PDF download and offline learning.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2 shrink-0">
                <button
                  onClick={() => window.print()}
                  className="bg-[#A7F3D0] hover:bg-[#86efac] text-emerald-950 font-extrabold px-5 py-2.5 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs flex items-center gap-2"
                >
                  <Printer className="w-4 h-4" />
                  <span>Print / Save as PDF</span>
                </button>

                <button
                  onClick={() => setActiveTab('videos')}
                  className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold px-4 py-2.5 rounded-xl border-2 border-black shadow-neo-xs text-xs flex items-center gap-1.5 transition-all"
                >
                  <Video className="w-4 h-4" />
                  <span>Watch Video</span>
                </button>

                {activeTopic.videos?.[0] && (
                  <a
                    href={activeTopic.videos[0].watch_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-white hover:bg-zinc-100 text-black font-extrabold px-3 py-2.5 rounded-xl border-2 border-black shadow-neo-xs text-xs flex items-center gap-1.5 transition-all"
                  >
                    <ExternalLink className="w-4 h-4" />
                    <span>YouTube</span>
                  </a>
                )}
              </div>
            </div>

            {/* Formatted Study Guide Document Container */}
            <div id="study-guide-printable" className="print-area bg-white border-3 border-black rounded-2xl p-6 sm:p-10 shadow-neo space-y-8">
              {/* Document Header */}
              <div className="border-b-3 border-black pb-6 space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono">
                  <div className="flex items-center gap-2">
                    <span className="font-extrabold uppercase bg-black text-[#FEF08A] px-2 py-0.5 rounded">
                      SkillForge AI Study Guide
                    </span>
                    <span className="font-bold text-zinc-600">
                      Track: {hubData?.course_title}
                    </span>
                  </div>
                  <div className="text-zinc-500 font-bold">
                    Est. Study Duration: {activeTopic.estimated_minutes} mins
                  </div>
                </div>

                <h1 className="text-3xl sm:text-4xl font-extrabold text-black">
                  {activeTopic.title}
                </h1>
                <p className="text-xs sm:text-sm text-zinc-600 font-medium">
                  {activeTopic.description}
                </p>
              </div>

              {/* 1. Executive Summary & Overview */}
              <div className="space-y-2">
                <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-1.5">
                  <BookOpen className="w-4 h-4 text-black" />
                  <span>1. Executive Summary & Core Principles</span>
                </h3>
                <div className="bg-[#FAF7F2] border-2 border-black rounded-xl p-5 text-sm text-zinc-800 font-medium leading-relaxed">
                  {activeTopic.study_notes.introduction}
                </div>
              </div>

              {/* 2. Key Concepts & Definitions */}
              {activeTopic.study_notes.concepts?.length > 0 && (
                <div className="space-y-3">
                  <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-1.5">
                    <Lightbulb className="w-4 h-4 text-amber-600" />
                    <span>2. Key Concepts & Technical Definitions</span>
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                    {activeTopic.study_notes.concepts.map((concept, i) => (
                      <div key={i} className="bg-white border-2 border-black rounded-xl p-4 shadow-neo-xs space-y-1.5">
                        <div className="font-extrabold text-sm text-black flex items-center gap-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shrink-0"></span>
                          <span>{concept.term}</span>
                        </div>
                        <p className="text-xs text-zinc-700 font-medium leading-relaxed">
                          {concept.definition}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 3. Step-by-Step Methodology */}
              {activeTopic.study_notes.step_by_step?.length > 0 && (
                <div className="space-y-3">
                  <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>3. Step-by-Step Practical Methodology</span>
                  </h3>
                  <div className="space-y-2.5">
                    {activeTopic.study_notes.step_by_step.map((step) => (
                      <div key={step.step} className="flex items-start gap-3 p-3.5 bg-zinc-50 border-2 border-black rounded-xl">
                        <div className="w-7 h-7 rounded-lg bg-black text-[#FEF08A] font-mono font-bold flex items-center justify-center shrink-0 text-xs">
                          {step.step}
                        </div>
                        <div className="space-y-0.5">
                          <h4 className="font-extrabold text-sm text-black">{step.title}</h4>
                          <p className="text-xs text-zinc-700 font-medium leading-relaxed">{step.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 4. Code & Architecture Blueprint */}
              {activeTopic.study_notes.code_example && (
                <div className="space-y-3">
                  <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-1.5">
                    <FileText className="w-4 h-4 text-black" />
                    <span>4. Technical Code Implementation & Blueprint</span>
                  </h3>
                  <div className="bg-zinc-950 text-emerald-400 font-mono text-xs sm:text-sm p-5 rounded-xl border-2 border-black overflow-x-auto leading-relaxed">
                    <pre>{activeTopic.study_notes.code_example.code}</pre>
                  </div>
                  <div className="bg-[#FAF7F2] border-2 border-black rounded-xl p-3.5 text-xs text-zinc-800 font-medium leading-relaxed">
                    <strong>Architectural Explanation:</strong> {activeTopic.study_notes.code_example.explanation}
                  </div>
                </div>
              )}

              {/* 5. Key Takeaways */}
              {activeTopic.study_notes.key_takeaways?.length > 0 && (
                <div className="bg-[#FEF08A]/40 border-2 border-black rounded-xl p-5 space-y-2.5">
                  <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-black">
                    5. Essential Takeaways & Mental Models
                  </h3>
                  <ul className="space-y-1.5">
                    {activeTopic.study_notes.key_takeaways.map((item, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-xs sm:text-sm font-medium text-black">
                        <span className="font-bold text-black leading-none">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* 6. Self-Assessment Practice Questions & Answers */}
              {activeTopic.study_notes.practice_questions?.length > 0 && (
                <div className="space-y-3">
                  <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-1.5">
                    <Brain className="w-4 h-4 text-black" />
                    <span>6. Practice Questions & Verified Explanations</span>
                  </h3>
                  <div className="space-y-3">
                    {activeTopic.study_notes.practice_questions.map((pq, idx) => (
                      <div key={idx} className="bg-zinc-50 border-2 border-black rounded-xl p-4 space-y-2">
                        <div className="font-extrabold text-sm text-black flex items-start gap-2">
                          <span className="w-5 h-5 rounded-full bg-black text-white font-mono text-xs flex items-center justify-center shrink-0">
                            {idx + 1}
                          </span>
                          <span>{pq.question}</span>
                        </div>
                        <div className="bg-[#A7F3D0]/60 border border-black rounded-lg p-3 text-xs font-medium text-emerald-950 space-y-1 ml-7">
                          <div><strong>Verified Answer:</strong> {pq.answer}</div>
                          <div><strong>Explanation:</strong> {pq.explanation}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 7. Recommended Video Lectures */}
              {activeTopic.videos?.length > 0 && (
                <div className="space-y-3">
                  <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-1.5">
                    <Video className="w-4 h-4 text-black" />
                    <span>7. Recommended Educational Video Lectures</span>
                  </h3>
                  <div className="space-y-2">
                    {activeTopic.videos.map((vid) => (
                      <div key={vid.id} className="p-3.5 bg-white border-2 border-black rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <span className="text-[10px] font-mono font-bold bg-[#FEF08A] px-2 py-0.5 rounded border border-black">
                              {vid.channel}
                            </span>
                            <span className="text-[10px] font-mono text-zinc-500 font-bold">
                              {vid.duration}
                            </span>
                          </div>
                          <div className="font-extrabold text-sm text-black">{vid.title}</div>
                          <p className="text-xs text-zinc-600 font-medium">{vid.summary}</p>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                          <button
                            onClick={() => setActiveTab('videos')}
                            className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold px-3 py-1.5 rounded-lg border border-black shadow-neo-xs text-xs flex items-center gap-1"
                          >
                            <Play className="w-3.5 h-3.5 fill-black" />
                            <span>Play Video</span>
                          </button>
                          <a
                            href={vid.watch_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-white hover:bg-zinc-100 text-black font-bold p-1.5 rounded-lg border border-black shadow-neo-xs text-xs flex items-center"
                          >
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Document Footer */}
              <div className="border-t-2 border-dashed border-zinc-300 pt-4 flex flex-wrap items-center justify-between text-xs font-mono text-zinc-500">
                <span>SkillForge AI • Personal AI Tutor & Adaptive Learning Platform</span>
                <span>Module ID: {activeTopic.id} • Ready for Diagnostic Validation</span>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: SMART NOTES (Course & Topic Scoped) */}
        {activeTab === 'smart_notes' && (
          <div className="space-y-6">
            {/* Smart Notes Header Banner */}
            <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo flex flex-wrap items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-mono font-bold bg-[#DDD6FE] px-2 py-0.5 rounded border border-black">
                    Student Notebook
                  </span>
                  <span className="text-xs font-mono font-bold text-zinc-500">
                    Learner ID: {learner?.id || 'demo-learner-1'}
                  </span>
                </div>
                <h2 className="text-2xl font-extrabold text-black">
                  Smart Notes for {hubData?.course_title}
                </h2>
                <p className="text-xs sm:text-sm text-zinc-600 font-medium">
                  Create, edit, and organize your private study notes by course and topic. Saved securely to your profile.
                </p>
              </div>

              {!isEditingNote && (
                <button
                  onClick={handleStartCreateNote}
                  className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold px-5 py-2.5 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs flex items-center gap-2"
                >
                  <Plus className="w-4 h-4" />
                  <span>Create New Note</span>
                </button>
              )}
            </div>

            {/* Note Editor Form */}
            {isEditingNote && (
              <div className="bg-[#FAF7F2] border-3 border-black rounded-2xl p-6 shadow-neo space-y-4">
                <div className="flex items-center justify-between border-b-2 border-black pb-3">
                  <h3 className="font-extrabold text-base text-black flex items-center gap-2">
                    <Edit className="w-4 h-4" />
                    <span>{editingNoteId ? 'Edit Smart Note' : 'Create New Smart Note'}</span>
                  </h3>
                  <button
                    onClick={handleCancelNote}
                    className="text-xs font-bold text-zinc-600 hover:text-black underline"
                  >
                    Cancel
                  </button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="sm:col-span-2 space-y-1">
                    <label className="text-xs font-mono font-bold uppercase text-zinc-700">Note Title</label>
                    <input
                      type="text"
                      value={noteTitle}
                      onChange={(e) => setNoteTitle(e.target.value)}
                      placeholder="e.g. Memory Mutability & Reference Semantics"
                      className="w-full bg-white border-2 border-black rounded-xl p-3 text-xs sm:text-sm font-bold text-black focus:outline-none focus:ring-2 focus:ring-yellow-400 shadow-neo-xs"
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs font-mono font-bold uppercase text-zinc-700">Topic</label>
                    <select
                      value={noteTopicId}
                      onChange={(e) => setNoteTopicId(e.target.value)}
                      className="w-full bg-white border-2 border-black rounded-xl p-3 text-xs sm:text-sm font-bold text-black focus:outline-none focus:ring-2 focus:ring-yellow-400 shadow-neo-xs"
                    >
                      {hubData?.topics?.map((t) => (
                        <option key={t.id} value={t.id}>{t.title}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-mono font-bold uppercase text-zinc-700">Note Content</label>
                  <textarea
                    rows={8}
                    value={noteContent}
                    onChange={(e) => setNoteContent(e.target.value)}
                    placeholder="Write key principles, code snippets, memory models, or questions..."
                    className="w-full bg-white border-2 border-black rounded-xl p-4 text-xs sm:text-sm font-medium text-black focus:outline-none focus:ring-2 focus:ring-yellow-400 shadow-neo-xs leading-relaxed"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    onClick={handleCancelNote}
                    className="bg-white hover:bg-zinc-100 text-zinc-800 font-bold px-4 py-2 rounded-xl border-2 border-black text-xs"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSaveNote}
                    className="bg-[#A7F3D0] hover:bg-[#86efac] text-emerald-950 font-extrabold px-6 py-2 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs"
                  >
                    {editingNoteId ? 'Save Changes' : 'Save Smart Note'}
                  </button>
                </div>
              </div>
            )}

            {/* Filter by Topic */}
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold text-zinc-600">Filter Notes:</span>
                <select
                  value={topicFilter}
                  onChange={(e) => setTopicFilter(e.target.value)}
                  className="bg-white text-xs font-mono font-bold text-black border border-black rounded-lg px-2.5 py-1 focus:outline-none shadow-neo-xs"
                >
                  <option value="all">All Topics ({notes.length})</option>
                  {hubData?.topics?.map((t) => (
                    <option key={t.id} value={t.id}>{t.title}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Saved Notes List */}
            {filteredNotes.length === 0 ? (
              <div className="bg-white border-3 border-black rounded-2xl p-10 text-center shadow-neo space-y-3">
                <div className="w-12 h-12 rounded-xl bg-zinc-100 border-2 border-black flex items-center justify-center mx-auto text-zinc-600">
                  <Edit3 className="w-6 h-6" />
                </div>
                <h3 className="text-base font-extrabold text-black">No Smart Notes Yet</h3>
                <p className="text-xs sm:text-sm text-zinc-600 font-medium max-w-sm mx-auto">
                  Record personal insights, code examples, or exam tips for this course. Click below to add your first note.
                </p>
                <button
                  onClick={handleStartCreateNote}
                  className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold px-4 py-2 rounded-xl border-2 border-black shadow-neo-xs text-xs inline-flex items-center gap-1.5"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Create First Note</span>
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredNotes.map((note) => (
                  <div
                    key={note.id}
                    className="bg-white border-3 border-black rounded-2xl p-5 shadow-neo flex flex-col justify-between space-y-3"
                  >
                    <div className="space-y-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-[10px] font-mono font-bold bg-[#DDD6FE] px-2 py-0.5 rounded border border-black truncate">
                          {note.topic_title || 'General'}
                        </span>
                        <span className="text-[10px] font-mono text-zinc-500">
                          {new Date(note.updated_at).toLocaleDateString()}
                        </span>
                      </div>

                      <h4 className="font-extrabold text-base text-black leading-snug">
                        {note.title}
                      </h4>

                      <p className="text-xs text-zinc-700 font-medium whitespace-pre-wrap leading-relaxed line-clamp-6">
                        {note.content}
                      </p>
                    </div>

                    <div className="border-t border-zinc-200 pt-3 flex items-center justify-end gap-2">
                      <button
                        onClick={() => handleStartEditNote(note)}
                        className="bg-zinc-50 hover:bg-zinc-100 text-zinc-800 text-xs font-bold px-3 py-1.5 rounded-lg border border-black shadow-neo-xs flex items-center gap-1 transition-all"
                      >
                        <Edit className="w-3.5 h-3.5" />
                        <span>Edit</span>
                      </button>

                      <button
                        onClick={() => setNoteToDelete(note)}
                        className="bg-rose-50 hover:bg-rose-100 text-rose-900 text-xs font-bold px-3 py-1.5 rounded-lg border border-black shadow-neo-xs flex items-center gap-1 transition-all"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                        <span>Delete</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Delete Confirmation Modal */}
            {noteToDelete && (
              <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo-lg max-w-md w-full space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-rose-200 border-2 border-black flex items-center justify-center shrink-0">
                      <AlertCircle className="w-5 h-5 text-rose-900" />
                    </div>
                    <div>
                      <h3 className="font-extrabold text-base text-black">Confirm Delete Note</h3>
                      <p className="text-xs text-zinc-600 font-medium">
                        Are you sure you want to delete <strong className="text-black">"{noteToDelete.title}"</strong>?
                      </p>
                    </div>
                  </div>

                  <p className="text-xs text-rose-950 font-medium bg-rose-50 p-3 rounded-lg border border-black">
                    This note will be permanently removed from your course notebook.
                  </p>

                  <div className="flex items-center justify-end gap-3 pt-2">
                    <button
                      onClick={() => setNoteToDelete(null)}
                      className="bg-white hover:bg-zinc-100 text-zinc-800 font-bold px-4 py-2 rounded-xl border-2 border-black text-xs"
                    >
                      Keep Note
                    </button>
                    <button
                      onClick={handleDeleteNoteConfirm}
                      className="bg-rose-600 hover:bg-rose-700 text-white font-extrabold px-5 py-2 rounded-xl border-2 border-black shadow-neo-xs text-xs"
                    >
                      Yes, Delete Note
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Persistent Bottom Attempt Test Banner */}
      <div className="bg-[#A7F3D0] border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg flex flex-wrap items-center justify-between gap-4">
        <div className="space-y-1">
          <span className="text-xs font-mono font-bold uppercase bg-black text-white px-2 py-0.5 rounded">
            Ready to Validate Mastery?
          </span>
          <h2 className="text-xl sm:text-2xl font-extrabold text-emerald-950">
            Take the {hubData?.course_title} Diagnostic Test
          </h2>
          <p className="text-xs sm:text-sm text-emerald-900 font-medium max-w-xl">
            Complete the adaptive assessment to benchmark your skills, unlock tailored challenge checkpoints, and verify your progression.
          </p>
        </div>

        <Link
          to={`/diagnostic?courseId=${activeCourseId}`}
          className="bg-black hover:bg-zinc-800 text-[#FEF08A] font-extrabold px-6 py-3.5 rounded-xl border-2 border-black shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-sm flex items-center gap-2"
        >
          <Brain className="w-5 h-5 text-[#FEF08A]" />
          <span>Attempt Test Now</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
};
