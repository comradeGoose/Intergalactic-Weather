var labels = [];
var series = [[]]

fetch('/weather/forecast?city=' + document.getElementById('location').textContent)
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

        var dataPlot = {
            labels: labels,
            series: series,
            // showPoint: true,
            // showLabel: false,
            // showArea: true,
        };
        var datalables = {
            labels: labels,
            series: series,
        }

        var options = {
            axisX: {
                offset: 30,
                position: 'end',
                labelOffset: {
                    x: -15,
                    y: 0
                },
                showLabel: true,
                showGrid: true,
                labelInterpolationFnc: Chartist.noop,
                type: undefined
            },
            axisY: {
                offset: 40,
                position: 'start',
                labelOffset: {
                    x: 0,
                    y: 0
                },
                showLabel: false,
                showGrid: true,
                labelInterpolationFnc: Chartist.noop,
                type: undefined,
                scaleMinSpace: 20,
                onlyInteger: false,
            },
            // width: 40,
            // height: '100%',
            showLine: true,
            showPoint: true,
            showArea: false,
            areaBase: 0,
            lineSmooth: true,
            showGridBackground: true,
            low: undefined,
            high: undefined,
            fullWidth: true,
            reverseData: false,
        };

        var optionsLabel = {
            axisX: {
                offset: 30,
                position: 'end',
                labelOffset: {
                    x: 0,
                    y: 0
                },
                showLabel: false,
                showGrid: false,
                labelInterpolationFnc: Chartist.noop,
                type: undefined
            },
            axisY: {
                offset: 40,
                position: 'start',
                labelOffset: {
                    x: 0,
                    y: 5
                },
                showLabel: true,
                showGrid: false,
                labelInterpolationFnc: Chartist.noop,
                type: undefined,
                scaleMinSpace: 20,
                onlyInteger: false,
                labelInterpolationFnc: function (value) {
                    return value + '°C';
                }
            },
            width: 40,
            height: undefined,
            showLine: false,
            showPoint: false,
            showArea: false,
            areaBase: 0,
            lineSmooth: false,
            showGridBackground: false,
            low: undefined,
            high: undefined,
            chartPadding: {
                top: 15,
                right: 15,
                bottom: 5,
                left: 10
            },
            fullWidth: false,
            reverseData: false,
        };

        new Chartist.Line('.temp-value', datalables, optionsLabel);
        new Chartist.Line('.ct-chart', dataPlot, options);

    })
    .catch(error => {
        console.error('Ошибка при запросе данных:', error);
    });
