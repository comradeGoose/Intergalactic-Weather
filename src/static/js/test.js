var labels = [];
var series = [[]]

fetch('/weather/forecast')
    .then(response => {
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        data.list.forEach(element => {
            labels.push(element.date);
            series[0].push(element.temp)
        });

        var data = {
            labels: labels,
            series: series
        };
        
        
        new Chartist.Line('.ct-chart', data);

    })
    .catch(error => {
        console.error('Ошибка при запросе данных:', error);
    });

