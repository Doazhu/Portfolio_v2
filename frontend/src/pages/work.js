import { useState, useEffect } from "react";
import "./work.css";
import Header from "../components/header";
import Footer from "../components/footer";
import WorkSlider from '../components/WorkSlider';
import { projectsAPI, uploadsAPI } from "../api";

function Work() {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadProjects = async () => {
            try {
                const data = await projectsAPI.getAll();
                setProjects(data);
            } catch (err) {
                console.error("Ошибка загрузки проектов:", err);
            } finally {
                setLoading(false);
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
                    <h2 className="accent-font">Другие работы</h2>
                    
                    {loading ? (
                        <div className="loading">Загрузка проектов...</div>
                    ) : projects.length === 0 ? (
                        <div className="no-projects">Проекты пока не добавлены</div>
                    ) : (
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
                    )}
                </section>
            </main>
            <Footer />
        </div>
    );
}

export default Work;
