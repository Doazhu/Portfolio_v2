import React from "react";
import { Link } from "react-router-dom";
import "./work.css";
import Header from "../components/header";
import Footer from "../components/footer";
import WorkSlider from '../components/WorkSlider';

function Work() {
  return (
    <div>
      <Header />
      <main>
        <h1 className="Work-text">Мои проекты</h1>
        <WorkSlider />
        <section className="krytaua-sectiya">

            <h1 className="Work-text">Мои остальные работы</h1>

          <div className="all-work">

            <div className="rows rows-1">
              <div>
                <div></div>
                <img src="http://localhost:3000/static/media/omlette_project.4329911993578898fb4a.jpg" />
                <h3>Omlette</h3>
                <p>моя первая работа, начало моей карьеры</p>
              </div>
              <div>
                <img src="http://localhost:3000/static/media/omlette_project.4329911993578898fb4a.jpg" />
                <h3>Проект 3</h3>
                <p>Описание проекта 3</p>
              </div>
            </div>

            <div className="rows rows-2">
              <div>
                <img src="http://localhost:3000/static/media/omlette_project.4329911993578898fb4a.jpg" />
                <h3>Проект 4</h3>
                <p>Описание проекта 4</p>
              </div>
              <div>
                <img src="http://localhost:3000/static/media/omlette_project.4329911993578898fb4a.jpg" />
                <h3>Проект 5</h3>
                <p>Описание проекта 5</p>
              </div>
            </div>

            <div className="rows rows-3">
              <div>
                <img src="http://localhost:3000/static/media/omlette_project.4329911993578898fb4a.jpg" />
                <h3>Проект 6</h3>
                <p>Описание проекта 6</p>
              </div>
              <div>
                <img src="http://localhost:3000/static/media/omlette_project.4329911993578898fb4a.jpg" />
                <h3>Проект 7</h3>
                <p>Описание проекта 7</p>
              </div>
              <div>
                <img src="http://localhost:3000/static/media/omlette_project.4329911993578898fb4a.jpg" />
                <h3>Проект 8</h3>
                <p>Описание проекта 8</p>
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
