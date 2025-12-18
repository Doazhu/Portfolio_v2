import React, { useState } from "react";
import "./contact.css";
import Header from "../components/header";
import Footer from "../components/footer";

function Contact() {
    const [copied, setCopied] = useState(null);

    const copyToClipboard = (text, type) => {
        navigator.clipboard.writeText(text);
        setCopied(type);
        setTimeout(() => setCopied(null), 2000);
    };

    const contacts = [
        {
            id: 'email',
            icon: '✉️',
            label: 'Email',
            value: 'me@doazhu.pro',
            link: 'mailto:me@doazhu.pro',
            color: '#EA4335'
        },
        {
            id: 'telegram',
            icon: '💬',
            label: 'Telegram',
            value: '@Doazhu',
            link: 'https://t.me/Doazhu',
            color: '#0088cc'
        },
        {
            id: 'vk',
            icon: '🔵',
            label: 'ВКонтакте',
            value: '@doazhu',
            link: 'https://vk.com/doazhu',
            color: '#4C75A3'
        },
        {
            id: 'github',
            icon: '🐙',
            label: 'GitHub',
            value: 'github.com/doazhu',
            link: 'https://github.com/doazhu',
            color: '#6e5494'
        }
    ];

    return (
        <div className="contact-page">
            <Header />
            <main className="contact-main">
                <div className="contact-hero">
                    <span className="contact-label">Связаться</span>
                    <h1 className="contact-title">
                        Давай создадим<br/>
                        что-то <span className="highlight">крутое</span>
                    </h1>
                    <p className="contact-subtitle">
                        Открыт для новых проектов, коллабораций и интересных идей
                    </p>
                </div>

                <div className="contact-grid">
                    {contacts.map((contact) => (
                        <a 
                            key={contact.id}
                            href={contact.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="contact-card"
                        >
                            <div className="contact-card-icon">{contact.icon}</div>
                            <div className="contact-card-info">
                                <span className="contact-card-label">{contact.label}</span>
                                <span className="contact-card-value">{contact.value}</span>
                            </div>
                            <div className="contact-card-arrow">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M7 17L17 7M17 7H7M17 7V17"/>
                                </svg>
                            </div>
                        </a>
                    ))}
                </div>

                <div className="contact-cta">
                    <div className="cta-card">
                        <div className="cta-emoji">🚀</div>
                        <h2>Есть идея?</h2>
                        <p>Напиши мне — обсудим детали и начнём работу</p>
                        <button 
                            className="cta-button"
                            onClick={() => copyToClipboard('me@doazhu.pro', 'email')}
                        >
                            {copied === 'email' ? '✓ Скопировано!' : 'Скопировать email'}
                        </button>
                    </div>

                    <div className="cta-card cta-fast">
                        <div className="cta-emoji">⚡</div>
                        <h2>Быстрый ответ</h2>
                        <p>Отвечаю в Telegram обычно в течение часа</p>
                        <a 
                            href="https://t.me/Doazhu" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="cta-button cta-telegram"
                        >
                            Написать в Telegram
                        </a>
                    </div>
                </div>

                <div className="contact-status">
                    <div className="status-dot"></div>
                    <span>Сейчас открыт для новых проектов</span>
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default Contact;
