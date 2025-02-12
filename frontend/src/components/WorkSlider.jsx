import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import project1 from "../images/library_project.jpg";
import project2 from "../images/portfolio_project.jpg";
import project3 from "../images/omlette_project.jpg";
import project4 from "../images/drive_project.jpg";
import './WorkSlider.css';

const works = [
    {
        id: 1,
        image: project2,
        title: "Моё старое портфолио",
        description: "Было множество версий моего первого портфолио, моя первая работа которую я начинал с Figma"
    },
    {
        id: 2,
        image: project1,
        title: "Библиотека",
        description: "Первая работа с фреймворком Django"
    },
    {
        id: 3,
        image: project3,
        title: "Рецепт отменного омлета",
        description: "Моя самая первая работа, начало моей карьеры "
    },
    {
        id: 4,
        image: project4,
        title: "Облако Fylo",
        description: "Красивый и простой стиль"
    },
    
];

const WorkSlider = () => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [touchStart, setTouchStart] = useState(0);
    const [direction, setDirection] = useState('next');

    useEffect(() => {
        const timer = setInterval(() => {
            setDirection('next');
            setCurrentIndex(prev => 
                prev === works.length - 1 ? 0 : prev + 1
            );
        }, 5000);
        return () => clearInterval(timer);
    }, []);

    const handleTouchStart = (e) => setTouchStart(e.touches[0].clientX);
    
    const handleTouchEnd = (e) => {
        const touchEnd = e.changedTouches[0].clientX;
        const diff = touchStart - touchEnd;
        if (Math.abs(diff) > 50) {
            const newDirection = diff > 0 ? 'next' : 'prev';
            setDirection(newDirection);
            setCurrentIndex(prev => 
                newDirection === 'next' 
                    ? (prev === works.length - 1 ? 0 : prev + 1)
                    : (prev === 0 ? works.length - 1 : prev - 1)
            );
        }
    };

    return (
        <div className="slider-container" 
             onTouchStart={handleTouchStart}
             onTouchEnd={handleTouchEnd}>
            
            <AnimatePresence mode="wait" custom={direction}>
                <motion.div
                    key={currentIndex}
                    className="slide"
                    custom={direction}
                    initial={{ opacity: 0, x: direction === 'next' ? 100 : -100 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: direction === 'next' ? -100 : 100 }}
                    transition={{ duration: 0.5 }}
                >
                    <div className="slide-content">
                        <motion.img 
                            src={works[currentIndex].image}
                            alt={works[currentIndex].title}
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{ duration: 0.5 }}
                        />
                        <div className="slide-info">
                            <motion.h2
                                initial={{ x: 50, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                transition={{ delay: 0.2 }}
                            >
                                {works[currentIndex].title}
                            </motion.h2>
                            <motion.p
                                initial={{ x: 50, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                transition={{ delay: 0.3 }}
                            >
                                {works[currentIndex].description}
                            </motion.p>
                        </div>
                    </div>
                </motion.div>
            </AnimatePresence>
            
            <div className="slider-dots">
                {works.map((_, index) => (
                    <button
                        key={index}
                        className={`dot ${index === currentIndex ? 'active' : ''}`}
                        onClick={() => setCurrentIndex(index)}
                    />
                ))}
            </div>
        </div>
    );
};

export default WorkSlider;