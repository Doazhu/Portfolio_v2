import React from 'react';
import './Timeline.css';

const Timeline = () => {
    const timelineItems = [
        {
            year: '~2 года назад',
            title: 'Начал изучать HTML и CSS',
            description: 'Основы верстки, адаптивный дизайн, первые шаги в веб-разработке',
        },
        {
            year: '~1.5 года назад',
            title: 'Первый проект на JavaScript',
            description: 'Создание интерактивного сайта с использованием HTML, CSS и JavaScript',
        },
        {
            year: '~1 год назад',
            title: 'Изучение Django',
            description: 'Серверная разработка, работа с базами данных, создание REST API',
        },
        {
            year: '~6 месяцев назад',
            title: 'Первый масштабный проект',
            description: 'Реализация сложного функционала, интеграция внешних API',
        },
        {
            year: '~3 месяца назад',
            title: 'FastAPI и React',
            description: 'Изучение современного стека для создания fullstack-приложений',
        },
    ];

    return (
        <section className="timeline-section">
            <h2>Мой путь</h2>
            <div className="timeline">
                {timelineItems.map((item, index) => (
                    <div key={index} className="timeline-item">
                        <div className="timeline-content">
                            <h3 className="timeline-title">{item.title}</h3>
                            <p className="timeline-description">{item.description}</p>
                            <span className="timeline-year">{item.year}</span>
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default Timeline;
