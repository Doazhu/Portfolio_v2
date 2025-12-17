import React from "react";
import "./work.css";
import Header from "../components/header";
import Footer from "../components/footer";
import WorkSlider from '../components/WorkSlider';
import omlette from "../images/omlette_project.jpg";
import library from "../images/library_project.jpg";
import portfolio from "../images/portfolio_project.jpg";
import drive from "../images/drive_project.jpg";

function Work() {
    return (
        <div>
            <Header />
            <main>
                <WorkSlider />
                
                <section className="other-works">
                    <h2>Другие работы</h2>
                    
                    <div className="works-grid">
                        <div className="work-card">
                            <img src={omlette} alt="Omlette" />
                            <div className="work-card-content">
                                <h3>Рецепт омлета</h3>
                                <p>Моя первая работа — простая landing page с рецептом</p>
                            </div>
                        </div>
                        
                        <div className="work-card">
                            <img src={library} alt="Library" />
                            <div className="work-card-content">
                                <h3>Библиотека</h3>
                                <p>Веб-приложение на Django с функционалом библиотеки</p>
                            </div>
                        </div>
                        
                        <div className="work-card">
                            <img src={portfolio} alt="Portfolio" />
                            <div className="work-card-content">
                                <h3>Старое портфолио</h3>
                                <p>Первая версия персонального сайта</p>
                            </div>
                        </div>
                        
                        <div className="work-card">
                            <img src={drive} alt="Fylo" />
                            <div className="work-card-content">
                                <h3>Облако Fylo</h3>
                                <p>Landing page с адаптивной вёрсткой</p>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
            <Footer />
        </div>
    );
}

export default Work;
