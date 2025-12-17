import React from "react";
import "./home.css";
import Header from "../components/header";
import SpiralRibbon from "../components/SpiralRibbon";
import { Link } from "react-router-dom";

function Home() {
    return (
        <div className="home-page">
            <SpiralRibbon />
            <Header />
            <main className="hero-main">
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
                
                <div className="scroll-hint fade-in-up">
                    <span>scroll</span>
                    <div className="scroll-line"></div>
                </div>
            </main>
        </div>
    );
}

export default Home;
