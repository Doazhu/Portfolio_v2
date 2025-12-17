import React from "react";
import { motion } from "framer-motion"; // импортируем motion для анимированных компонентов
import "./about.css";
import image from "../images/about.png";
import Header from "../components/header";
import Timeline from '../components/Timeline';
import Footer from '../components/footer';

function About() {
  // Варианты анимаций. Можно регулировать по желанию.
  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: (i) => ({
      opacity: 1,
      y: 0,
      transition: { delay: i * 0.2, duration: 0.5 }
    }),
  };

  return (
    <div>
      <Header />
      <main>
        {/* Анимированный раздел "Обо мне" */}
        <motion.section 
          className="about-section"
          initial="hidden"
          animate="visible"
          variants={containerVariants}
        >
          <div className="image-container">
            <motion.img 
              src={image} 
              alt="image"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <div className="about-text">
            <motion.h1 variants={itemVariants} custom={0}>Я Александр</motion.h1>
            <motion.p variants={itemVariants} custom={1}>
              На протяжении последнего года я активно развиваюсь в области программирования и цифрового дизайна.
              Моя страсть - открывать новые горизонты, будь то путешествия в новые страны или изучение передовых технологий.
              Этот подход помогает мне не только расширять кругозор, но и находить вдохновение для создания проектов.
              Я горжусь тем, что всего за год сделал множество самостоятельных проектов, которые помогли мне понять фундаментальные принципы разработки и применить их на практике.
              Постоянное стремление к обучению стало неотъемлемой частью моего пути - я всегда ищу новые вызовы, которые помогут мне расти как разработчику и творческому человеку.
            </motion.p>
            <motion.p variants={itemVariants} custom={2}>
              Помимо программирования, я увлечен кулинарией, которая, как и кодинг, требует точности, экспериментов и креативности.
              Эти качества помогают мне находить баланс между работой, учебой и личными интересами.
              Я убежден, что развитие - это бесконечный процесс, и с каждым шагом я становлюсь ближе к своим целям. Для меня важно не стоять на месте, учиться новому и создавать что-то значимое.
            </motion.p>
          </div>
        </motion.section>

        <motion.div 
          className="timeline-container"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <Timeline />
        </motion.div>

        <motion.h1 
          className="skills-title"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          Мой подход
        </motion.h1>

        {/* Анимированный раздел "Навыки" */}
        <motion.section 
          className="skills-section"
          initial="hidden"
          animate="visible"
          variants={containerVariants}
        >
          <div className="skills-container">
            {/** Можно анимировать каждый элемент списка, передавая custom-параметр для задержки */}
            {[
              {
                id: 0,
                title: "Сделаю это",
                description: `Я начинающий full-stack разработчик, готовый воплотить идеи в жизнь с использованием таких фреймворков, как FastAPI, React, Django и технологий HTML5/CSS3.
                Моя сила — в создании функциональных прототипов и надежных решений, которые остаются гибкими для дальнейшей доработки и масштабирования.
                Я верю, что качественный код — это основа для успешного проекта, поэтому каждая деталь оттачивается с вниманием к потребностям конечного пользователя.`,
              },
              {
                id: 1,
                title: "Сотрудничество",
                description: `Настоящий успех приходит тогда, когда работа ведется в тесном сотрудничестве. Я открыт для диалога и активно привлекаю команду и заказчиков к совместному процессу разработки.
                Вместе мы сможем создать продукт, который не только удовлетворяет технические требования, но и превосходит ожидания пользователей.
                Ваши идеи и обратная связь помогут превратить любой проект в инновационное решение.`,
              },
              {
                id: 2,
                title: "Доступность для всех",
                description: `Разрабатывая проекты, я ставлю во главу угла доступность и удобство использования. Это не просто тренд — это необходимость, чтобы технологии работали для каждого.
                Применяя принципы адаптивного дизайна и оптимизации, я стремлюсь создать интерфейсы, которые понятны и удобны, независимо от того, кто ими пользуется.`,
              },
              {
                id: 3,
                title: "Я продолжаю экспериментировать",
                description: `Каждый проект — это возможность для обучения и экспериментов. Я не боюсь новых идей и тщательно анализирую результаты, чтобы улучшать свои навыки.
                Даже если что-то не получается с первого раза, я всегда извлекаю уроки и готов двигаться дальше, создавая всё более совершенные и масштабируемые решения.`,
              },
            ].map((item, index) => (
              <motion.div 
                key={item.id} 
                className="skills-item"
                variants={itemVariants}
                custom={index}
              >
                <b>{item.id}</b>
                <h2>{item.title}</h2>
                <p>{item.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>
      </main>
      <Footer />
    </div>
  );
}

export default About;
