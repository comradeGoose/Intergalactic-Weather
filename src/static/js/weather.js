// Ваши данные о температуре


const data = [
    { date: '2023-01-01 00:00', temperature: 9 },
    { date: '2023-01-01 03:00', temperature: 11 },
    { date: '2023-01-01 06:00', temperature: 15 },
    { date: '2023-01-01 09:00', temperature: 16 },
    { date: '2023-01-01 12:00', temperature: 20 },
    { date: '2023-01-01 15:00', temperature: 22 },
    { date: '2023-01-01 18:00', temperature: 21 },
    // Добавьте остальные значения
];



for (let index = 0; index < 40; index++) {
    var date = new Date('2023-01-01 00:00');
    date.setHours(3*index);
    if (date.getHours() === 0) {
        const monthName = date.toLocaleString('default', { month: 'long' });
        console.log(monthName + ' ' + date.getDate());
    }
    else {
        console.log(date.getHours() + ':' + date.getMinutes);
    }
}
    


// for (let index = 0; index < 40; index++) {

//     data.push({new Date()})
    
// }

// Получение элемента canvas
const canvas = document.getElementById('temperatureChart');
const ctx = canvas.getContext('2d');

// Размеры холста и масштаб
const canvasWidth = canvas.width;
const canvasHeight = canvas.height;
const scale = canvasWidth / (data.length - 1);

// Функция для рисования графика
function drawChart() {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    // Отрисовка линии графика
    ctx.beginPath();
    for (let i = 0; i < data.length; i++) {
        const x = i * scale;
        const y = canvasHeight - (data[i].temperature * 2) * 4; // Масштабируем для более яркой визуализации
        ctx.lineTo(x, y);

        // Отображение меток времени
        ctx.fillText(data[i].date, x, y + 20);

        // Отображение меток температур
        ctx.fillText(data[i].temperature + "°C", x, y - 10);
    }
    ctx.strokeStyle = 'blue';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Отрисовка оси X
    ctx.beginPath();
    ctx.moveTo(0, canvasHeight);
    ctx.lineTo(canvasWidth, canvasHeight);
    ctx.stroke();

    // Отрисовка оси Y
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, canvasHeight);
    ctx.stroke();
}

// Вызов функции для отрисовки графика
drawChart();