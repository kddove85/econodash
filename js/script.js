function drawgraph(id, startAtZero, new_labels, values, maximum) {
  var barData = {
    labels: new_labels,
    datasets : [{
      fillColor: "rgba(151,187,205,0.2)",
      strokeColor: "rgba(151,187,205,1)",
      pointColor: "rgba(151,187,205,1)",
      data: values,
    }]
   }
   var mychart = document.getElementById(id).getContext("2d");
    var myBarChart = new Chart(mychart, {
    type: 'bar',
    data: barData,
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: startAtZero
                }
            }]
        },
        legend: {
            display: false
        }
    }
});
}
function set_data(legends, values, colors) {
    console.log(legends);
    var datasets = [];
    for (i = 0; i < legends.length; i++) {
        console.log(i);
        var dict = {};
        dict['label'] = legends[i];
        dict['backgroundColor'] = colors[i];
        dict['data'] = values[i];
        datasets.push(dict);
    };
    console.log(datasets);
    return datasets;
};

function new_drawgraph(id, startAtZero, new_labels, legends, values, colors) {
    var my_datasets = set_data(legends, values, colors)
    new Chart(document.getElementById(id), {
        type: 'bar',
        data: {
          labels: new_labels,
          datasets: my_datasets
        },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                      major: {
                        enabled: true,
                        fontColor: '#FF5733'
                      }
//                    max: 30000000,
//                    min: 0,
//                    stepSize: 3000000,
//                    beginAtZero: true
                }
            }]
        },
     }
})
console.log(my_datasets)
};
