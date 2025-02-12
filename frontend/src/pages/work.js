import React from "react";
import { Link } from "react-router-dom";
import "./work.css";
import Header from "../components/header";
import Footer from "../components/footer";
import WorkSlider from '../components/WorkSlider';



function Work() {
  return (
    <body>
      <Header />
      <main>
        <h1 className="Work-text">Мои проекты</h1>
        <WorkSlider />
      </main>
      <Footer />
    </body>
  );
}

export default Work;
