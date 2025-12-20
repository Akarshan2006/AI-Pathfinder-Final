import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { FiBookOpen, FiArrowRight, FiClock, FiWifi, FiWifiOff, FiGithub, FiExternalLink, FiVideo } from 'react-icons/fi';

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const LearningTab = () => {
    const [learningPrompt, setLearningPrompt] = useState("");
    const [learningResult, setLearningResult] = useState(null);
    const [learningLoading, setLearningLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isOnline, setIsOnline] = useState(navigator.onLine);

    useEffect(() => {
        const handleOnline = () => setIsOnline(true);
        const handleOffline = () => setIsOnline(false);

        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);

        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, []);

    const generateLearning = async () => {
        setLearningLoading(true);
        setError(null);
        setLearningResult(null);
        try {
            const res = await axios.post(`${API}/learning`, { prompt: learningPrompt });
            setLearningResult(res.data);
        } catch (e) {
            console.error(e);
            setError("Could not reach backend. Make sure FastAPI is running and you have an internet connection.");
        } finally {
            setLearningLoading(false);
        }
    };

    const offlineContent = (
        <div className="text-center mt-10">
            <FiWifiOff className="mx-auto text-5xl text-slate-500 mb-4" />
            <h3 className="text-2xl font-bold text-slate-300">You are currently offline</h3>
            <p className="text-slate-400">Some features are disabled. Pre-loaded learning paths are available below.</p>
            {/* Here you could display a list of pre-loaded learning paths */}
        </div>
    );

    return (
        <div>
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-semibold flex items-center gap-2">
                    <FiBookOpen /> Learning Path Generator
                </h2>
                <div className={`flex items-center gap-2 text-sm font-semibold ${isOnline ? 'text-green-400' : 'text-red-400'}`}>
                    {isOnline ? <FiWifi /> : <FiWifiOff />}
                    <span>{isOnline ? 'Online' : 'Offline'}</span>
                </div>
            </div>
            
            <p className="text-slate-400 mb-4">Enter a skill or a role you want to learn, and AI will generate a roadmap.</p>
            
            {error && (
                <div className="bg-red-500/20 text-red-300 p-3 rounded-lg mb-4">
                    {error}
                </div>
            )}

            <div className="flex gap-3">
                <input
                    value={learningPrompt}
                    onChange={(e) => setLearningPrompt(e.target.value)}
                    className="input-field flex-grow"
                    placeholder="e.g. 'Learn React for web development' or 'Become a Data Scientist'"
                    disabled={!isOnline}
                />
                <button
                    onClick={generateLearning}
                    className="primary-btn flex items-center gap-2"
                    disabled={learningLoading || !isOnline}
                >
                    {learningLoading ? "Generating..." : "Generate"}
                    {!learningLoading && <FiArrowRight />}
                </button>
            </div>

            {!isOnline && offlineContent}

            {learningResult && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-8">
                    <h3 className="text-xl font-semibold mb-3">Your AI-Generated Learning Path for "{learningResult.prompt}"</h3>
                    <p className="text-slate-400 mb-4 flex items-center gap-2"><FiClock /> Estimated Duration: <span className="font-semibold text-violet-300">{learningResult.estimated_duration}</span></p>

                    <div className="space-y-4">
                        {learningResult.path.map((step, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ x: -20, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                transition={{ delay: idx * 0.15 }}
                                className="p-4 bg-slate-900/50 border-l-4 border-violet-500 rounded-r-lg"
                            >
                                <div className="font-bold text-xl mb-2">{idx + 1}. {step.title}</div>
                                <p className="text-slate-300 ml-6 mb-3">{step.description}</p>
                                <div className="text-xs font-semibold uppercase text-violet-400/80 ml-6 mb-4">{step.difficulty}</div>
                                
                                {step.resources && (
                                    <div className="ml-6 border-t border-slate-700 pt-3">
                                        <h4 className="text-sm font-bold text-slate-300 mb-2">Resources:</h4>
                                        <div className="flex flex-col gap-2">
                                            {step.resources.tutorials?.[0] && <a href={step.resources.tutorials[0]} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-sm text-sky-400 hover:underline"><FiExternalLink /> Tutorial</a>}
                                            {step.resources.github_projects?.[0] && <a href={step.resources.github_projects[0]} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-sm text-slate-400 hover:underline"><FiGithub /> GitHub Project</a>}
                                            {step.resources.videos?.[0] && <a href={step.resources.videos[0]} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-sm text-pink-400 hover:underline"><FiVideo /> Code with Harry / Apna College</a>}
                                        </div>
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            )}
        </div>
    );
};

export default LearningTab;
