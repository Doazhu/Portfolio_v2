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
                        <motion.h1 variants={itemVariants} custom={0}>Я Александр</motion.h1>
                        <motion.p variants={itemVariants} custom={1}>
                            На протяжении последних пяти лет я активно развиваюсь в области программирования и цифрового дизайна.
                            Моя страсть — открывать новые горизонты, будь то путешествия в новые страны или изучение передовых технологий.
                            Этот подход помогает мне не только расширять кругозор, но и находить вдохновение для создания проектов.
                        </motion.p>
                        <motion.p variants={itemVariants} custom={2}>
                            Я горжусь тем, что за эти годы сделал более сотни проектов, которые помогли мне понять фундаментальные принципы разработки и применить их на практике.
                            Постоянное стремление к обучению стало неотъемлемой частью моего пути — я всегда ищу новые вызовы, которые помогут мне расти как разработчику и творческому человеку.
                        </motion.p>
                        <motion.p variants={itemVariants} custom={3}>
                            Помимо программирования, я увлечен кулинарией, которая, как и кодинг, требует точности, экспериментов и креативности.
                            Эти качества помогают мне находить баланс между работой, учебой и личными интересами.
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

                <motion.h1 
                    className="skills-title"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                >
                    Мой подход
                </motion.h1>

                <motion.section 
                    className="skills-section"
                    initial="hidden"
                    animate="visible"
                    variants={containerVariants}
                >
                    <div className="skills-container">
                        {[
                            {
                                id: 0,
                                title: "Сделаю это",
                                description: `Я full-stack разработчик, готовый воплотить идеи в жизнь с использованием FastAPI, React, Django и технологий HTML5/CSS3. Моя сила — в создании функциональных решений, которые остаются гибкими для масштабирования.`,
                            },
                            {
                                id: 1,
                                title: "Сотрудничество",
                                description: `Настоящий успех приходит тогда, когда работа ведется в тесном сотрудничестве. Я открыт для диалога и активно привлекаю заказчиков к совместному процессу разработки.`,
                            },
                            {
                                id: 2,
                                title: "Доступность для всех",
                                description: `Разрабатывая проекты, я ставлю во главу угла доступность и удобство использования. Применяю принципы адаптивного дизайна и оптимизации для всех устройств.`,
                            },
                            {
                                id: 3,
                                title: "Эксперименты",
                                description: `Каждый проект — это возможность для обучения и экспериментов. Я не боюсь новых идей и тщательно анализирую результаты, чтобы улучшать свои навыки.`,
                            },
                        ].map((item, index) => (
                            <motion.div 
                                key={item.id} 
                                className="skills-item"
                                variants={itemVariants}
                                custom={index}
                            >
                                <b>{item.id}</b>
                                <h2>{item.title}</h2>
                                <p>{item.description}</p>
                            </motion.div>
                        ))}
                    </div>
                </motion.section>
            </main>
            <Footer />
        </div>
    );
}

export default About;
