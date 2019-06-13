/*
    Place here your plots configs for Chart.js
*/

// default point radius
Chart.defaults.global.defaultFontColor = '#aaa';
Chart.defaults.global.defaultFontSize = '20';
Chart.defaults.global.elements.point.radius = 0;
Chart.defaults.global.elements.point.hitRadius = 1;
Chart.defaults.global.elements.point.hoverBorderWidth = 1;


// debug
function print(msg) {
    console.log(msg)
}

// config line styled plot
function configTimeSeries(plot) {
    return {
        type: plot.type,
        data: {
            labels: plot.labels,
            datasets: plot.datasets
        },
        options: {
            maintainAspectRatio: false,
            tooltips: {enabled: false},
            hover: {mode: 'dataset', intersect: false},
            legend: false,
            responsive: true,
            title: {
                display: false,
                text: plot.title
            },

            scales: {
                xAxes: [
                    {
                        type: "time",
                        scaleLabel: {
                            display: true,
                            labelString: plot.xAxisName
                        },
                        gridLines: {
                            borderDash: [1, 1],
                            color: "#aaa"
                        },
                        ticks: {
                            autoSkip: true,
                            maxTicksLimit: 12,
                            fontFamily: "'Lato', 'Helvetica Neue', Arial",
                            fontSize: '16',
                            fontColor: '#aaa'
                        },
                        time: {
                            displayFormats: {
                                'millisecond': 'MMM DD',
                                'second': 'MMM DD',
                                'minute': 'MMM DD',
                                'hour': 'MMM DD',
                                'day': 'MMM DD',
                                'week': 'MMM DD',
                                'month': 'MMM DD',
                                'quarter': 'MMM DD',
                                'year': 'MMM DD',
                            }
                        }
                    }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: plot.yAxisName
                        },
                        gridLines: {
                            borderDash: [1, 1],
                            color: "#aaa"
                        },
                        ticks: {
                            fontFamily: "'Lato', 'Helvetica Neue', Arial",
                            fontSize: '16',
                            fontColor: '#aaa'
                        }
                    }
                ]
            }
        }
    };
}


