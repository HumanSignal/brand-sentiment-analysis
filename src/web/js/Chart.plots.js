/*
    Place here your plots configs for Chart.js
*/

// default point radius
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
                            color: "#ddd"
                        },
                        ticks: {
                            autoSkip: true,
                            maxRotation: 75,
                            minRotation: 75,
                            maxTicksLimit: 12,
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
                            color: "#ddd"
                        }
                    }
                ]
            },

            pan: {
                enabled: true,
                mode: "xy",
                speed: 10,
                threshold: 10
            }
        }
    };
}


