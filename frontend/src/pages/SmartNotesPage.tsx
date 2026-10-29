import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useLearner } from '../context/LearnerContext';
import { Layers, Upload, Sparkles, BookOpen, FileText, CheckCircle2, ArrowRight, Eye } from 'lucide-react';

export const SmartNotesPage: React.FC = () => {
  const { showToast } = useLearner();
  const [documents, setDocuments] = useState<any[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<any | null>(null);
  const [uploading, setUploading] = useState(false);
  const [generatingTools, setGeneratingTools] = useState(false);
  const [generatedResult, setGeneratedResult] = useState<any | null>(null);

  const fetchDocs = async () => {
    try {
      const docs = await api.getDocuments();
      setDocuments(docs);
      if (docs.length > 0 && !selectedDoc) {
        setSelectedDoc(docs[0]);
      }
    } catch (err: any) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      setUploading(true);
      const res = await api.uploadDocument(file);
      showToast(`Extracted ${res.key_concepts.length} concepts from ${res.filename}!`, 'success');
      await fetchDocs();
      setSelectedDoc(res);
    } catch (err: any) {
      showToast(`Upload failed: ${err.message}`, 'error');
    } finally {
      setUploading(false);
    }
  };

  const handleGenerateStudyTools = async () => {
    if (!selectedDoc) return;
    try {
      setGeneratingTools(true);
      const tools = await api.generateStudyTools(selectedDoc.id);
      setGeneratedResult(tools);
      showToast(`Generated ${tools.flashcards.length} flashcards and ${tools.generated_quizzes.length} quiz questions!`, 'success');
    } catch (err: any) {
      showToast(err.message, 'error');
    } finally {
      setGeneratingTools(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo-lg">
        <div className="inline-flex items-center gap-2 bg-[#A7F3D0] text-black text-xs font-mono font-bold px-3 py-1 rounded-full border border-black mb-3">
          <Layers className="w-3.5 h-3.5" />
          <span>Smart Notes & Syllabus Ingestion</span>
        </div>
        <h1 className="text-3xl font-extrabold text-black">Document Concept Extractor & Revision Tools</h1>
        <p className="text-sm text-zinc-600 mt-1 max-w-2xl font-medium">
          Upload course notes, textbook excerpts, or syllabus files (PDF / TXT). SkillForge AI automatically extracts core technical concepts, builds structured summaries, and synthesizes interactive flashcards & practice quizzes.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Upload Column */}
        <div className="space-y-6">
          <div className="bg-white border-3 border-black rounded-2xl p-6 shadow-neo">
            <h2 className="text-lg font-extrabold text-black mb-4 flex items-center gap-2">
              <Upload className="w-5 h-5 text-black" />
              <span>Upload Document</span>
            </h2>

            <label className="border-2 border-dashed border-black hover:border-black bg-zinc-50 hover:bg-[#FEF08A]/30 transition-all rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer text-center block">
              <FileText className="w-10 h-10 text-zinc-500 mb-2" />
              <span className="text-sm font-extrabold text-black">
                {uploading ? 'Extracting Text & Concepts...' : 'Choose PDF or TXT File'}
              </span>
              <span className="text-xs text-zinc-500 mt-1 font-mono">Max size: 10MB • ground truth citations</span>
              <input
                type="file"
                accept=".pdf,.txt,.md"
                onChange={handleFileUpload}
                disabled={uploading}
                className="hidden"
              />
            </label>

            {/* Uploaded Documents List */}
            {documents.length > 0 && (
              <div className="mt-6 border-t-2 border-black pt-4">
                <div className="text-xs font-mono font-bold text-zinc-500 uppercase tracking-wider mb-2">
                  Ingested Notes ({documents.length})
                </div>
                <div className="space-y-2 max-h-60 overflow-y-auto">
                  {documents.map((doc) => (
                    <button
                      key={doc.id}
                      onClick={() => setSelectedDoc(doc)}
                      className={`w-full text-left p-2.5 rounded-lg border-2 transition-all flex items-center justify-between text-xs ${
                        selectedDoc?.id === doc.id
                          ? 'bg-[#DDD6FE] border-black font-bold shadow-neo-xs'
                          : 'bg-zinc-50 hover:bg-zinc-100 border-black'
                      }`}
                    >
                      <div className="truncate pr-2">
                        <div className="font-bold text-black truncate">{doc.filename}</div>
                        <div className="text-[10px] text-zinc-500">{doc.file_type} • {doc.char_count} chars</div>
                      </div>
                      <Eye className="w-4 h-4 text-zinc-600 shrink-0" />
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Selected Document Details & Extracted Concepts */}
        <div className="lg:col-span-2 space-y-6">
          {selectedDoc ? (
            <div className="bg-white border-3 border-black rounded-2xl p-6 sm:p-8 shadow-neo space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-4 border-b-2 border-black pb-4">
                <div>
                  <div className="text-xs font-mono font-bold text-zinc-500 uppercase">Selected Document</div>
                  <h2 className="text-2xl font-extrabold text-black">{selectedDoc.filename}</h2>
                </div>
                <button
                  onClick={handleGenerateStudyTools}
                  disabled={generatingTools}
                  className="bg-[#FEF08A] hover:bg-[#fde047] text-black font-extrabold px-4 py-2.5 rounded-xl border-2 border-black shadow-neo-xs hover:translate-x-0.5 hover:translate-y-0.5 transition-all text-xs flex items-center gap-1.5"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>{generatingTools ? 'Generating...' : 'Generate Flashcards & Quiz'}</span>
                </button>
              </div>

              {/* Summary */}
              <div className="bg-[#FAF7F2] border-2 border-black rounded-xl p-4">
                <div className="text-xs font-mono font-bold text-zinc-500 uppercase mb-1">
                  Structured Pedagogical Summary
                </div>
                <p className="text-xs sm:text-sm text-zinc-800 leading-relaxed font-medium">
                  {selectedDoc.summary}
                </p>
              </div>

              {/* Extracted Key Concepts */}
              <div>
                <h3 className="text-lg font-extrabold text-black mb-3">
                  Identified Key Concepts ({selectedDoc.key_concepts?.length || 0})
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {selectedDoc.key_concepts?.map((c: any, idx: number) => (
                    <div key={idx} className="bg-zinc-50 border-2 border-black rounded-xl p-3.5 shadow-neo-xs">
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="font-extrabold text-sm text-black">{c.term}</span>
                        <span className="text-[10px] font-mono font-bold bg-[#A7F3D0] text-emerald-900 px-2 py-0.5 rounded border border-black">
                          {c.importance}
                        </span>
                      </div>
                      <p className="text-xs text-zinc-700 leading-normal font-medium">
                        {c.definition}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Generated Tools Preview if available */}
              {generatedResult && (
                <div className="border-t-2 border-black pt-6 space-y-4">
                  <div className="bg-[#DDD6FE] border-2 border-black rounded-xl p-4 flex items-center justify-between">
                    <div>
                      <h4 className="font-extrabold text-sm text-black">Study Tools Generated!</h4>
                      <p className="text-xs text-zinc-700">
                        {generatedResult.flashcards.length} Flashcards and {generatedResult.generated_quizzes.length} Diagnostic Questions created.
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <a href="/revision" className="bg-black text-[#FEF08A] font-bold text-xs px-3 py-1.5 rounded border border-black shadow-neo-xs">
                        Open Flashcards
                      </a>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-white border-3 border-black rounded-2xl p-12 text-center shadow-neo">
              <FileText className="w-12 h-12 text-zinc-400 mx-auto mb-3" />
              <h3 className="text-lg font-extrabold text-black">No Document Selected</h3>
              <p className="text-xs text-zinc-600 mt-1">Upload a PDF or TXT file or select Scenario #10 from the top banner to inspect notes extraction.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
