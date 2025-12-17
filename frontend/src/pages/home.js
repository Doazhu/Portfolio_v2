import React, { useEffect, useState, useRef } from "react";
import "./home.css";
import Header from "../components/header";
import SpiralRibbon from "../components/SpiralRibbon";
import { Link } from "react-router-dom";

function Home() {
    const [headerVisible, setHeaderVisible] = useState(true);
    const [isScrolled, setIsScrolled] = useState(false);
    const lastScrollY = useRef(0);
    const containerRef = useRef(null);

    useEffect(() => {
        const container = containerRef.current;
        if (!container) return;

        let ticking = false;

        const handleScroll = () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    const currentScrollY = container.scrollTop;
                    
                    setIsScrolled(currentScrollY > 50);
                    
                    if (currentScrollY > lastScrollY.current && currentScrollY > 100) {
                        setHeaderVisible(false);
                    } else {
                        setHeaderVisible(true);
                    }
                    
                    lastScrollY.current = currentScrollY;
                    ticking = false;
                });
                ticking = true;
            }
        };

        container.addEventListener('scroll', handleScroll, { passive: true });
        return () => container.removeEventListener('scroll', handleScroll);
    }, []);

    const scrollToNext = () => {
        containerRef.current?.scrollTo({
            top: window.innerHeight,
            behavior: 'smooth'
        });
    };

    return (
        <div className="home-page" ref={containerRef}>
            <SpiralRibbon />
            
            <div className={`header-wrapper ${headerVisible ? 'visible' : 'hidden'} ${isScrolled ? 'scrolled' : ''}`}>
                <Header />
            </div>
            
            <section className="hero-section">
                <div className="hero-content">
                    <h1 className="hero-title fade-in-up">
                        <span className="greeting">Привет</span>
                        <span className="wave">👋</span>
                    </h1>
                    
                    <p className="hero-subtitle fade-in-up">
                        Я <span className="highlight">Александр</span>, fullstack разработчик
                    </p>
                    
                    <p className="hero-tagline fade-in-up">
                        Создаю решения, которые вдохновляют
                    </p>

                    <Link to="/about" className="hero-cta fade-in-up">
                        <span>Узнать больше</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M7 17L17 7M17 7H7M17 7V17"/>
                        </svg>
                    </Link>
                </div>
                
                <button className="scroll-hint fade-in-up" onClick={scrollToNext}>
                    <span>scroll</span>
                    <div className="scroll-line"></div>
                </button>
            </section>

            <section className="showcase-section">
                <div className="showcase-content">
                    <div className="showcase-text">
                        <span className="showcase-label">Что я делаю</span>
                        <h2 className="showcase-title">
                            Превращаю идеи<br/>в <span className="highlight">код</span>
                        </h2>
                        <p className="showcase-description">
                            От концепта до продакшена. Фронтенд, бэкенд, 
                            дизайн — всё в одних руках.
                        </p>
                    </div>
                    
                    <div className="showcase-stats">
                        <div className="stat-item">
                            <span className="stat-number">2+</span>
                            <span className="stat-label">года в разработке</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-number">10+</span>
                            <span className="stat-label">проектов</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-number">∞</span>
                            <span className="stat-label">желание учиться</span>
                        </div>
                    </div>
                </div>
                
                <div className="showcase-cta">
                    <Link to="/work" className="showcase-link">
                        Смотреть работы
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M5 12h14M12 5l7 7-7 7"/>
                        </svg>
                    </Link>
                </div>
            </section>
        </div>
    );
}

export default Home;
