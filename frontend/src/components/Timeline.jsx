import React from 'react';
import { motion } from 'framer-motion';
import './Timeline.css';

const Timeline = () => {
    const timelineItems = [
        {
            year: '~5 лет назад',
            title: 'Начал изучать HTML и CSS',
            description: 'Основы верстки, адаптивный дизайн, первые шаги в веб-разработке',
        },
        {
            year: '~4.5 года назад',
            title: 'Первый проект на JavaScript',
            description: 'Создание интерактивного сайта с использованием HTML, CSS и JavaScript',
        },
        {
            year: '~4 года назад',
            title: 'Изучение Django',
            description: 'Серверная разработка, работа с базами данных, создание REST API',
        },
        {
            year: '~3 года назад',
            title: 'Первый масштабный проект',
            description: 'Реализация сложного функционала, интеграция внешних API',
        },
        {
            year: '~2.5 года назад',
            title: 'FastAPI и React',
            description: 'Изучение современного стека для создания fullstack-приложений',
        },
        {
            year: '~1 год назад',
            title: 'Выход на фриланс',
            description: 'Первые коммерческие заказы, работа с реальными клиентами и дедлайнами',
        },
    ];

    const itemVariants = {
        hidden: (isEven) => ({
            opacity: 0,
            x: isEven ? 50 : -50,
        }),
        visible: {
            opacity: 1,
            x: 0,
            transition: {
                duration: 0.6,
                ease: "easeOut"
            }
        }
    };

    const dotVariants = {
        hidden: { scale: 0, opacity: 0 },
        visible: { 
            scale: 1, 
            opacity: 1,
            transition: { duration: 0.3 }
        }
    };

    return (
        <section className="timeline-section">
            <motion.h2
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ duration: 0.5 }}
            >
                Мой путь
            </motion.h2>
            <div className="timeline">
                {timelineItems.map((item, index) => (
                    <motion.div 
                        key={index} 
                        className="timeline-item"
                        custom={index % 2 === 1}
                        variants={itemVariants}
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true, margin: "-50px" }}
                    >
                        <motion.div 
                            className="timeline-dot"
                            variants={dotVariants}
                            initial="hidden"
                            whileInView="visible"
                            viewport={{ once: true }}
                        />
                        <motion.div 
                            className="timeline-content"
                            whileHover={{ 
                                y: -4, 
                                boxShadow: "0 0 30px rgba(204, 255, 0, 0.15)" 
                            }}
                        >
                            <h3 className="timeline-title">{item.title}</h3>
                            <p className="timeline-description">{item.description}</p>
                            <span className="timeline-year">{item.year}</span>
                        </motion.div>
                    </motion.div>
                ))}
                
                <motion.div 
                    className="timeline-item timeline-continue"
                    initial={{ opacity: 0, scale: 0.8 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true, margin: "-50px" }}
                    transition={{ duration: 0.6, ease: "easeOut" }}
                >
                    <motion.div 
                        className="timeline-dot"
                        variants={dotVariants}
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                    />
                    <motion.div 
                        className="timeline-content timeline-future"
                        whileHover={{ 
                            scale: 1.02,
                            borderColor: "var(--toxic-yellow)",
                            backgroundColor: "rgba(204, 255, 0, 0.05)"
                        }}
                    >
                        <motion.div 
                            className="future-icon"
                            animate={{ y: [0, -10, 0] }}
                            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                        >
                            🚀
                        </motion.div>
                        <h3 className="timeline-title">И это только начало...</h3>
                        <p className="timeline-description">
                            Впереди новые технологии, масштабные проекты и бесконечный рост
                        </p>
                    </motion.div>
                </motion.div>
            </div>
        </section>
    );
};

export default Timeline;
