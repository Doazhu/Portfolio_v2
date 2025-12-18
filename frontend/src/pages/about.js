import React from "react";
import { motion } from "framer-motion";
import "./about.css";
import image from "../images/about.png";
import Header from "../components/header";
import Timeline from '../components/Timeline';
import Footer from '../components/footer';

function About() {
    const containerVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 30 },
        visible: (i) => ({
            opacity: 1,
            y: 0,
            transition: { delay: i * 0.15, duration: 0.5 }
        }),
    };

    const approaches = [
        {
            id: '00',
            icon: '⚡',
            title: 'Сделаю это',
            description: 'Full-stack разработка на FastAPI, React, Django. Функциональные решения, готовые к масштабированию.',
            accent: '#CCFF00'
        },
        {
            id: '01',
            icon: '🤝',
            title: 'Сотрудничество',
            description: 'Открыт для диалога. Вместе создаём продукт, который превосходит ожидания.',
            accent: '#00FF88'
        },
        {
            id: '02',
            icon: '📱',
            title: 'Адаптивность',
            description: 'Pixel-perfect на любом устройстве. Mobile-first подход и оптимизация производительности.',
            accent: '#00CCFF'
        },
        {
            id: '03',
            icon: '🔬',
            title: 'Эксперименты',
            description: 'Каждый проект — возможность для роста. Новые технологии, свежие решения.',
            accent: '#FF6B00'
        },
    ];

    return (
        <div>
            <Header />
            <main>
                <motion.section 
                    className="about-section"
                    initial="hidden"
                    animate="visible"
                    variants={containerVariants}
                >
                    <div className="image-container">
                        <motion.div 
                            className="image-card"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.5 }}
                        >
                            <img src={image} alt="Александр" />
                            <p className="image-card-label">
                                <span>@doazhu</span> — это я
                            </p>
                        </motion.div>
                    </div>
                    
                    <div className="about-text">
                        <motion.h1 variants={itemVariants} custom={0}><span className="accent-font">Я Александр</span></motion.h1>
                        <motion.p variants={itemVariants} custom={1}>
                            На протяжении последних пяти лет я активно развиваюсь в области программирования и цифрового дизайна.
                            Моя страсть — открывать новые горизонты, будь то путешествия в новые страны или изучение передовых технологий.
                        </motion.p>
                        <motion.p variants={itemVariants} custom={2}>
                            Я горжусь тем, что за эти годы сделал более сотни проектов, которые помогли мне понять фундаментальные принципы разработки и применить их на практике.
                        </motion.p>
                        <motion.p variants={itemVariants} custom={3}>
                            Помимо программирования, я увлечен кулинарией, которая, как и кодинг, требует точности, экспериментов и креативности.
                        </motion.p>
                    </div>
                </motion.section>

                <motion.div 
                    className="timeline-container"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.8 }}
                >
                    <Timeline />
                </motion.div>

                <section className="approach-section">
                    <motion.div 
                        className="approach-header"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.5 }}
                    >
                        <span className="approach-label">Как я работаю</span>
                        <h2 className="approach-title accent-font">Мой подход</h2>
                    </motion.div>

                    <div className="approach-grid">
                        {approaches.map((item, index) => (
                            <motion.div 
                                key={item.id}
                                className="approach-card"
                                initial={{ opacity: 0, y: 40 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true, margin: "-50px" }}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                                whileHover={{ y: -8 }}
                                style={{ '--accent': item.accent }}
                            >
                                <div className="approach-card-header">
                                    <span className="approach-number">{item.id}</span>
                                    <span className="approach-icon">{item.icon}</span>
                                </div>
                                <h3 className="approach-card-title">{item.title}</h3>
                                <p className="approach-card-text">{item.description}</p>
                                <div className="approach-card-line"></div>
                            </motion.div>
                        ))}
                    </div>
                </section>
            </main>
            <Footer />
        </div>
    );
}

export default About;
