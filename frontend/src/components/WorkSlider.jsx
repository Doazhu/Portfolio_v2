import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect, useCallback } from 'react';
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
        description: "Множество версий моего первого портфолио — от макета в Figma до рабочего сайта. Первый опыт создания персонального сайта."
    },
    {
        id: 2,
        image: project1,
        title: "Библиотека",
        description: "Первый проект на Django с полноценным CRUD функционалом, авторизацией пользователей и работой с базой данных."
    },
    {
        id: 3,
        image: project3,
        title: "Рецепт отменного омлета",
        description: "Моя самая первая вёрстка — простая страница, с которой началась карьера в веб-разработке."
    },
    {
        id: 4,
        image: project4,
        title: "Облако Fylo",
        description: "Landing page с современным дизайном и адаптивной вёрсткой. Практика работы с Flexbox и Grid."
    },
];

const WorkSlider = () => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [direction, setDirection] = useState(1);

    const goNext = useCallback(() => {
        setDirection(1);
        setCurrentIndex(prev => (prev === works.length - 1 ? 0 : prev + 1));
    }, []);

    const goPrev = useCallback(() => {
        setDirection(-1);
        setCurrentIndex(prev => (prev === 0 ? works.length - 1 : prev - 1));
    }, []);

    useEffect(() => {
        const timer = setInterval(goNext, 6000);
        return () => clearInterval(timer);
    }, [goNext]);

    const slideVariants = {
        enter: (dir) => ({ x: dir > 0 ? 300 : -300, opacity: 0 }),
        center: { x: 0, opacity: 1 },
        exit: (dir) => ({ x: dir > 0 ? -300 : 300, opacity: 0 })
    };

    return (
        <section className="slider-section">
            <h2>Мои работы</h2>
            <div className="slider-container">
                <AnimatePresence mode="wait" custom={direction}>
                    <motion.div
                        key={currentIndex}
                        className="slide"
                        custom={direction}
                        variants={slideVariants}
                        initial="enter"
                        animate="center"
                        exit="exit"
                        transition={{ duration: 0.4, ease: "easeInOut" }}
                    >
                        <div className="slide-content">
                            <div className="slide-image-wrapper">
                                <motion.img
                                    src={works[currentIndex].image}
                                    alt={works[currentIndex].title}
                                    initial={{ scale: 0.95, opacity: 0 }}
                                    animate={{ scale: 1, opacity: 1 }}
                                    transition={{ duration: 0.4 }}
                                />
                            </div>
                            <div className="slide-info">
                                <motion.h2
                                    initial={{ y: 20, opacity: 0 }}
                                    animate={{ y: 0, opacity: 1 }}
                                    transition={{ delay: 0.15 }}
                                >
                                    {works[currentIndex].title}
                                </motion.h2>
                                <motion.p
                                    initial={{ y: 20, opacity: 0 }}
                                    animate={{ y: 0, opacity: 1 }}
                                    transition={{ delay: 0.25 }}
                                >
                                    {works[currentIndex].description}
                                </motion.p>
                            </div>
                        </div>
                    </motion.div>
                </AnimatePresence>

                <div className="slider-nav">
                    <button className="slider-arrow" onClick={goPrev} aria-label="Previous">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M15 18l-6-6 6-6" />
                        </svg>
                    </button>
                    
                    <div className="slider-dots">
                        {works.map((_, index) => (
                            <button
                                key={index}
                                className={`dot ${index === currentIndex ? 'active' : ''}`}
                                onClick={() => {
                                    setDirection(index > currentIndex ? 1 : -1);
                                    setCurrentIndex(index);
                                }}
                                aria-label={`Slide ${index + 1}`}
                            />
                        ))}
                    </div>
                    
                    <button className="slider-arrow" onClick={goNext} aria-label="Next">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M9 18l6-6-6-6" />
                        </svg>
                    </button>
                </div>
            </div>
        </section>
    );
};

export default WorkSlider;
