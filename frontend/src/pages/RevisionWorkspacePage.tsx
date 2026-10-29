import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { Flashcard } from '../types';
import { Layers, RotateCcw, Check, Sparkles, Brain, ArrowLeft, ArrowRight } from 'lucide-react';

export const RevisionWorkspacePage: React.FC = () => {
  const { activeScenarioId, showToast } = useLearner();
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchFlashcards = async () => {
    try {
      setLoading(true);
      const cards = await api.getFlashcards();
      setFlashcards(cards);
      setCurrentIndex(0);
      setIsFlipped(false);
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFlashcards();
  }, [activeScenarioId]);

  const currentCard = flashcards[currentIndex];

  const handleRate = async (confidence: 'learning' | 'mastered') => {
    if (!currentCard) return;
    try {
      await api.reviewFlashcard(currentCard.id, confidence);
      showToast(`Marked as ${confidence}!`, 'success');
      setIsFlipped(false);
      if (currentIndex < flashcards.length - 1) {
        setCurrentIndex(prev => prev + 1);
      } else {
        showToast('You completed this revision session!', 'info');
      }
    } catch (err: any) {
      showToast(err.message, 'error');
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 bg-[#DDD6FE] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black mb-2">
            <Layers className="w-3.5 h-3.5" />
            <span>Spaced Repetition & Revision</span>
          </div>
          <h1 className="text-3xl font-extrabold text-black">Interactive Flashcard Desk</h1>
          <p className="text-xs sm:text-sm text-zinc-600 font-medium">
            Active recall workspace generated from smart notes and core skill definitions.
          </p>
        </div>
        <div className="text-xs font-mono font-bold bg-[#FEF08A] px-3 py-1.5 rounded-lg border-2 border-black shadow-neo-xs">
          Card {flashcards.length > 0 ? currentIndex + 1 : 0} of {flashcards.length}
        </div>
      </div>

      {/* Main Flashcard 3D Card */}
      {flashcards.length > 0 && currentCard ? (
        <div className="space-y-6">
          <div
            onClick={() => setIsFlipped(!isFlipped)}
            className="w-full min-h-[320px] bg-white border-3 border-black rounded-3xl p-8 sm:p-12 shadow-neo-lg cursor-pointer hover:shadow-neo hover:translate-x-0.5 hover:translate-y-0.5 transition-all flex flex-col justify-between text-center select-none"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold bg-black text-[#FEF08A] px-2.5 py-0.5 rounded">
                {currentCard.skill_code}
              </span>
              <span className="text-xs font-mono font-bold text-zinc-500 uppercase">
                {isFlipped ? 'Answer (Click to flip)' : 'Prompt (Click to reveal)'}
              </span>
            </div>

            <div className="my-auto py-6">
              <div className="text-xl sm:text-2xl font-extrabold text-black leading-snug">
                {isFlipped ? currentCard.back : currentCard.front}
              </div>
              {isFlipped && currentCard.source_concept && (
                <div className="mt-4 text-xs font-mono text-zinc-500">
                  Concept Source: <strong className="text-black">{currentCard.source_concept}</strong>
                </div>
              )}
            </div>

            <div className="text-xs font-mono text-zinc-400">
              Reviewed {currentCard.review_count} times • Confidence: {currentCard.confidence}
            </div>
          </div>

          {/* Action rating buttons when flipped */}
          <div className="flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => handleRate('learning')}
              className="bg-[#FED7AA] hover:bg-[#fdba74] text-black font-extrabold px-6 py-3 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs sm:text-sm flex items-center gap-2"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Still Learning (Review Again)</span>
            </button>
            <button
              onClick={() => handleRate('mastered')}
              className="bg-[#A7F3D0] hover:bg-[#6ee7b7] text-black font-extrabold px-6 py-3 rounded-xl border-2 border-black shadow-neo-sm hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs sm:text-sm flex items-center gap-2"
            >
              <Check className="w-4 h-4 text-emerald-800" />
              <span>Mastered (Move to Next)</span>
            </button>
          </div>

          {/* Navigation Controls */}
          <div className="flex items-center justify-between pt-4">
            <button
              disabled={currentIndex === 0}
              onClick={() => {
                setIsFlipped(false);
                setCurrentIndex(prev => Math.max(0, prev - 1));
              }}
              className="bg-white hover:bg-zinc-100 disabled:opacity-40 border-2 border-black px-4 py-2 rounded-xl text-xs font-bold shadow-neo-xs flex items-center gap-1.5"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>
            <button
              disabled={currentIndex === flashcards.length - 1}
              onClick={() => {
                setIsFlipped(false);
                setCurrentIndex(prev => Math.min(flashcards.length - 1, prev + 1));
              }}
              className="bg-white hover:bg-zinc-100 disabled:opacity-40 border-2 border-black px-4 py-2 rounded-xl text-xs font-bold shadow-neo-xs flex items-center gap-1.5"
            >
              <span>Next</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-white border-3 border-black rounded-2xl p-12 text-center shadow-neo">
          <Layers className="w-12 h-12 text-zinc-400 mx-auto mb-3" />
          <h3 className="text-lg font-extrabold text-black">No Active Flashcards</h3>
          <p className="text-xs text-zinc-600 mt-1">Upload notes on the Smart Notes page or switch to Scenario #10 to load neural network revision flashcards.</p>
        </div>
      )}
    </div>
  );
};
