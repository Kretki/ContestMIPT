//document.addEventListener("DOMContentLoaded", function(){
//    const sidePercent = 20; // Процент ширины для бокового контейнера
//
//    const leftContainer = document.querySelector('.side-circles.left');
//    const rightContainer = document.querySelector('.side-circles.right');
//
//    // Устанавливаем ширину контейнеров в зависимости от переменной sidePercent
//    leftContainer.style.width = sidePercent + '%';
//    rightContainer.style.width = sidePercent + '%';
//
//    // Функция для генерации случайного процента от 0 до 100
//    function randomPercentage() {
//        return Math.random() * 100;
//    }
//
//    const numCircles = 100;
//
//    // Генерация 100 кружков для левой стороны
//    for (let i = 0; i < numCircles; i++) {
//        let circle = document.createElement('div');
//        circle.classList.add('circle');
//        circle.style.position = 'absolute';
//        circle.style.top = randomPercentage() + '%';
//        circle.style.left = randomPercentage() + '%';
//        leftContainer.appendChild(circle);
//    }
//
//    // Генерация 100 кружков для правой стороны
//    for (let i = 0; i < numCircles; i++) {
//        let circle = document.createElement('div');
//        circle.classList.add('circle');
//        circle.style.position = 'absolute';
//        circle.style.top = randomPercentage() + '%';
//        circle.style.right = randomPercentage() + '%';
//        rightContainer.appendChild(circle);
//    }
//});


document.addEventListener("DOMContentLoaded", function () {
    ScrollReveal().reveal('.section-title', { delay: 200, origin: 'top', distance: '30px' });
    ScrollReveal().reveal('.section-description', { delay: 400, origin: 'bottom', distance: '30px' });
    ScrollReveal().reveal('.feature-card', { delay: 600, interval: 200, origin: 'bottom', distance: '50px' });
    ScrollReveal().reveal('.leaderboard li', { delay: 500, interval: 200, origin: 'right', distance: '40px' });
});