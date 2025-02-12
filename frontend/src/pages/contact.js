import React from "react";
import "./contact.css";
import Header from "../components/header";
import Footer from "../components/footer";

function Contact() {
    return (
        <body>
            <Header />
        <div className="contact-section">
            <h1>Связь со мной</h1>
            <p>Свяжитесь со мной, если у вас есть вопросы или предложения.</p>
            <p>Мои контакты:</p>
            <p>Email: <a href="mailto:alexandrrenev07@gmail.com">alexandrrenev07@gmail.com</a></p>
            <p>Телеграм: <a href="https://t.me/Doazhu">@Doazhu</a></p>
            <p>ВКонтакте: <a href="https://vk.com/doazhu">@Doazhu</a></p>
        </div>
        <Footer />
        </body>
    );
}

export default Contact;
