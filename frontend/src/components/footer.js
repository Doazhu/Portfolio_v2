import React from "react";
import "./footer.css";
import vk from "../images/VK_white.svg";
import telegram from "../images/Telegram_white.svg";
import github from "../images/Github_white.svg";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h2 className="footer-title">Doazhu</h2>
          <p className="footer-text">
            Спасибо, что посетили мой сайт! Здесь вы можете узнать больше обо мне и моих работах.
          </p>
          <div className="footer-social-icons">
            <a href="https://vk.com/doazhu"><img src={vk} alt="Vk" className="footer-icon" /></a>
            <a href="https://t.me/Doazhu"><img src={telegram} alt="Telegram" className="footer-icon" /></a>
            <a href="https://github.com/Doazhu"><img src={github} alt="Github" className="footer-icon" /></a>
          </div>
        </div>

        <div className="footer-section">
          <h3 className="footer-subtitle">Навигация</h3>
          <ul className="footer-nav-list">
            <li className="footer-nav-item">
              <a href="/" className="footer-link">Home</a>
            </li>
            <li className="footer-nav-item">
              <a href="/contact" className="footer-link">Contact</a>
            </li>
            <li className="footer-nav-item">
              <a href="/about" className="footer-link">About</a>
            </li>
          </ul>
        </div>

        <div className="footer-section">
          <h3 className="footer-subtitle">Контакты</h3>
          <p className="footer-text">Email: alexanderrenev07@gmail.com</p>
          <p className="footer-text">Website: doazhu.ru</p>
        </div>

        <div className="footer-section">
          <h3 className="footer-subtitle">Получайте новости</h3>
          <form className="footer-form">
            <input type="email" placeholder="Ваш email" className="footer-input" />
            <button className="footer-button">Подписаться</button>
          </form>
        </div>
      </div>

      <div className="footer-bottom">
        <p className="footer-text">© 2025 Doazhu. Все права защищены.</p>
      </div>
    </footer>
  );
};

export default Footer;
