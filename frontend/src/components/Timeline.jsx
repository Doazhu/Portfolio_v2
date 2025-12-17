import React from 'react';
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
                
                <div className="timeline-item timeline-continue">
                    <div className="timeline-content timeline-future">
                        <div className="future-icon">🚀</div>
                        <h3 className="timeline-title">И это только начало...</h3>
                        <p className="timeline-description">
                            Впереди новые технологии, масштабные проекты и бесконечный рост
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Timeline;
