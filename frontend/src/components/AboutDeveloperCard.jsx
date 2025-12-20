import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiGithub, FiLinkedin, FiMail, FiCode } from 'react-icons/fi';

const avatarStyles = [
    'bottts', 'initials', 'thumbs', 'shapes', 
    'adventurer', 'big-ears', 'micah', 'fun-emoji'
];

const AboutDeveloperCard = ({ developer, index }) => {
    const [avatarStyle, setAvatarStyle] = useState(avatarStyles[0]);

    const changeAvatar = () => {
        setAvatarStyle(prevStyle => {
            let newIndex;
            do {
                newIndex = Math.floor(Math.random() * avatarStyles.length);
            } while (avatarStyles[newIndex] === prevStyle);
            return avatarStyles[newIndex];
        });
    };

    const cardVariants = {
        hidden: { opacity: 0, y: 50, scale: 0.9 },
        visible: {
            opacity: 1,
            y: 0,
            scale: 1,
            transition: {
                delay: index * 0.3,
                duration: 0.6,
                ease: "easeOut"
            }
        }
    };

    return (
        <motion.div
            variants={cardVariants}
            className="relative group w-full"
        >
            <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg blur opacity-25 group-hover:opacity-100 transition duration-1000 group-hover:duration-200 animate-tilt"></div>
            <div className="relative p-6 bg-slate-900 rounded-lg leading-none flex flex-col h-full">
                <div className="flex items-center justify-between mb-4">
                    <motion.div
                        className="relative cursor-pointer"
                        whileHover={{ scale: 1.1 }}
                        onClick={changeAvatar}
                    >
                        <AnimatePresence mode="wait">
                            <motion.img
                                key={avatarStyle}
                                src={`https://api.dicebear.com/8.x/${avatarStyle}/svg?seed=${developer.name}`}
                                alt={developer.name}
                                className="w-20 h-20 rounded-full border-2 border-slate-700"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1, rotate: [0, 5, 0, -5, 0] }}
                                exit={{ opacity: 0 }}
                                transition={{ duration: 0.5 }}
                            />
                        </AnimatePresence>
                        <motion.div
                            className="absolute inset-0 rounded-full"
                            style={{
                                boxShadow: '0 0 20px 5px rgba(192, 132, 252, 0)',
                            }}
                            animate={{
                                boxShadow: [
                                    '0 0 20px 5px rgba(192, 132, 252, 0)',
                                    '0 0 20px 10px rgba(192, 132, 252, 0.5)',
                                    '0 0 20px 5px rgba(192, 132, 252, 0)',
                                ],
                            }}
                            transition={{
                                duration: 2,
                                ease: "easeInOut",
                                repeat: Infinity,
                            }}
                        />
                    </motion.div>
                    <motion.div 
                        className="flex items-center gap-2 text-purple-400 font-semibold"
                        whileHover={{ scale: 1.1 }}
                    >
                        <FiCode className="animate-pulse" />
                        <span className="text-sm">Dev</span>
                    </motion.div>
                </div>
                <div>
                    <h4 className="text-2xl font-bold text-white" style={{ fontFamily: "'Sora', sans-serif" }}>{developer.name}</h4>
                    <p className="text-purple-400 font-semibold mb-3 text-lg" style={{ textShadow: '0 0 10px rgba(192, 132, 252, 0.5)' }}>{developer.role}</p>
                </div>
                <p className="text-slate-400 text-sm mb-4 flex-grow">{developer.contributions}</p>
                <div className="mb-4">
                    <h5 className="font-bold text-slate-300 mb-2 text-sm uppercase tracking-wider">Core Expertise</h5>
                    <div className="flex flex-wrap gap-2">
                        {developer.skills.split(', ').map(skill => (
                            <motion.span 
                                key={skill} 
                                className="bg-slate-800 text-slate-300 text-xs font-semibold px-3 py-1 rounded-full"
                                whileHover={{ scale: 1.1, backgroundColor: '#5b21b6' }}
                            >
                                {skill}
                            </motion.span>
                        ))}
                    </div>
                </div>
                <div className="mt-auto flex justify-center gap-6 text-slate-500">
                    <a href={developer.github} target="_blank" rel="noopener noreferrer" className="hover:text-purple-400 transition-colors"><FiGithub size={22} /></a>
                    <a href={developer.linkedin} target="_blank" rel="noopener noreferrer" className="hover:text-purple-400 transition-colors"><FiLinkedin size={22} /></a>
                    <a href={`mailto:${developer.email}`} className="hover:text-purple-400 transition-colors"><FiMail size={22} /></a>
                </div>
            </div>
        </motion.div>
    );
};


export default AboutDeveloperCard;
