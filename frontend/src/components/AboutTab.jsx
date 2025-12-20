import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { FiUsers, FiCoffee, FiAward } from 'react-icons/fi';
import AboutDeveloperCard from './AboutDeveloperCard';

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const AboutTab = () => {
    const [developers, setDevelopers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDevelopers = async () => {
            try {
                const response = await axios.get(`${API}/candidates`);
                const devs = response.data.filter(c => c.is_developer);
                
                // Manually set roles here for demonstration
                devs[0].role = "Backend Designer";
                devs[1].role = "UI Frontend Design";

                setDevelopers(devs);
            } catch (error) {
                console.error("Failed to fetch developers:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchDevelopers();
    }, []);

    if (loading) {
        return <div className="text-center p-8">Loading...</div>;
    }

    return (
        <div className="relative text-white p-4 md:p-8 min-h-[80vh] overflow-hidden bg-slate-900">
            <div className="absolute inset-0 w-full h-full bg-gradient-to-b from-slate-900 to-gray-900"></div>
            <div className="absolute inset-0 w-full h-full bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-5"></div>


            <motion.div
                initial="hidden"
                animate="visible"
                variants={{
                    visible: { transition: { staggerChildren: 0.2 } }
                }}
                className="relative z-10 space-y-24"
            >
                {/* Header Section */}
                <motion.div 
                    className="text-center"
                    variants={{ hidden: { opacity: 0, y: -50 }, visible: { opacity: 1, y: 0 } }}
                    transition={{ duration: 0.7 }}
                >
                    <h2 className="text-4xl md:text-6xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600 leading-tight" style={{ fontFamily: "'Sora', sans-serif" }}>
                        The Genesis of AI PathFinder
                    </h2>
                    <p className="mt-4 text-slate-300 max-w-3xl mx-auto text-lg" style={{ fontFamily: "'Inter', sans-serif" }}>
                        A fusion of code and ambition, AI PathFinder is a testament to the power of developer collaboration. This project harnesses AI to illuminate career paths and empower professional growth.
                    </p>
                    <p className="mt-2 text-purple-400 text-md" style={{ fontFamily: "'Inter', sans-serif" }}>
                        <FiAward className="inline-block mr-2" />
                        Proudly developed by students of AIML CSE, TIT Bhopal.
                    </p>
                </motion.div>

                {/* Developers Section */}
                <motion.div 
                    variants={{
                        visible: { transition: { staggerChildren: 0.3 } }
                    }}
                >
                    <h3 className="text-3xl font-bold text-center mb-12 flex items-center justify-center gap-3 text-slate-200" style={{ fontFamily: "'Sora', sans-serif" }}>
                        <FiUsers /> Meet the Architects
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-10 max-w-5xl mx-auto">
                        {developers.map((dev, index) => (
                            <AboutDeveloperCard key={dev.id} developer={dev} index={index} />
                        ))}
                    </div>
                </motion.div>

                {/* Donation Section */}
                <motion.div 
                    variants={{ hidden: { opacity: 0, scale: 0.8 }, visible: { opacity: 1, scale: 1 } }}
                    transition={{ duration: 0.5 }}
                    className="flex justify-center"
                >
                     <div className="relative group">
                        <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg blur-2xl opacity-50 group-hover:opacity-100 transition duration-1000 group-hover:duration-200 animate-pulse"></div>
                        <div className="relative bg-slate-900/90 backdrop-blur-sm rounded-xl p-8 border border-slate-800 text-center">
                            <FiCoffee className="mx-auto text-purple-400 text-4xl mb-4" />
                            <h3 className="text-3xl font-bold mb-2 text-white" style={{ fontFamily: "'Sora', sans-serif" }}>
                                Fuel Our Mission
                            </h3>
                            <p className="text-slate-400 mb-5 max-w-md mx-auto" style={{ fontFamily: "'Inter', sans-serif" }}>
                                If our work has inspired you, consider supporting our journey. Every contribution fuels future innovation.
                            </p>
                            <div className="inline-block bg-slate-800 p-4 rounded-lg border border-slate-700">
                                <p className="font-mono text-xl text-purple-300 tracking-widest">forcoffee@developer.webapp</p>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </motion.div>
        </div>
    );
};

export default AboutTab;

