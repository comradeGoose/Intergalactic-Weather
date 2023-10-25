var weatherData = [];
console.log(weatherData);

fetch('/weather/forecast')
    .then(response => {
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        weatherData = data.list;
    })
    .catch(error => {
        console.error('Ошибка при запросе данных:', error);
    });

weatherData.forEach(element => {
    console.log(element.date + ' ~~~ ' + element.temp);
});

var data = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    series: [
        [2, 3, 2, 4, 5],
        [0, 2.5, 3, 2, 3],
        [1, 2, 2.5, 3.5, 4]
    ]
};


new Chartist.Line('.ct-chart', data);

