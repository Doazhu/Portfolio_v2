import React, { useState, useEffect } from "react";
import "./work.css";
import Header from "../components/header";
import Footer from "../components/footer";
import WorkSlider from '../components/WorkSlider';
import { projectsAPI, uploadsAPI } from "../api";
import omlette from "../images/omlette_project.jpg";
import library from "../images/library_project.jpg";
import portfolio from "../images/portfolio_project.jpg";
import drive from "../images/drive_project.jpg";

const fallbackWorks = [
    { id: 1, image_url: omlette, title: "Рецепт омлета", description: "Моя первая работа — простая landing page с рецептом" },
    { id: 2, image_url: library, title: "Библиотека", description: "Веб-приложение на Django с функционалом библиотеки" },
    { id: 3, image_url: portfolio, title: "Старое портфолио", description: "Первая версия персонального сайта" },
    { id: 4, image_url: drive, title: "Облако Fylo", description: "Landing page с адаптивной вёрсткой" },
];

function Work() {
    const [projects, setProjects] = useState(fallbackWorks);

    useEffect(() => {
        const loadProjects = async () => {
            try {
                const data = await projectsAPI.getAll();
                if (data.length > 0) {
                    setProjects(data);
                }
            } catch (err) {
                console.log("Используем fallback данные");
            }
        };
        loadProjects();
    }, []);

    const getImageUrl = (project) => {
        if (!project.image_url) return null;
        if (project.image_url.startsWith("http") || project.image_url.startsWith("data:")) {
            return project.image_url;
        }
        return uploadsAPI.getUrl(project.image_url);
    };

    return (
        <div>
            <Header />
            <main>
                <WorkSlider />
                
                <section className="other-works">
                    <h2>Другие работы</h2>
                    
                    <div className="works-grid">
                        {projects.filter(p => !p.is_featured).map(project => (
                            <div className="work-card" key={project.id}>
                                {project.image_url && (
                                    <img src={getImageUrl(project)} alt={project.title} />
                                )}
                                <div className="work-card-content">
                                    <h3>{project.title}</h3>
                                    <p>{project.description}</p>
                                    {project.tech_stack && (
                                        <span className="tech-stack">{project.tech_stack}</span>
                                    )}
                                    <div className="work-card-links">
                                        {project.github_url && (
                                            <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                                                GitHub
                                            </a>
                                        )}
                                        {project.live_url && (
                                            <a href={project.live_url} target="_blank" rel="noopener noreferrer">
                                                Demo
                                            </a>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            </main>
            <Footer />
        </div>
    );
}

export default Work;
