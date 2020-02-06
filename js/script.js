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
function set_data(legends, values) {
    console.log(legends);
        var datasets = [];
            for (i in legends) {
                console.log(i);
                var dict = [];
                dict.push({
                    key:   "label",
                    value: i
                });
                dict.push({
                    key:   "backgroundColor",
                    value: "#3e95cd"
                });
                dict.push({
                    key:   "data",
                    value: values
                });
                datasets.push(dict)
            };
        console.log(datasets);
        return datasets;
      };

function new_drawgraph(id, startAtZero, new_labels, legends, values) {
    console.log(id);
    console.log(startAtZero);
    console.log(new_labels);
    console.log(legends);
    console.log(values);
    var datasets = []
    new Chart(document.getElementById(id), {
        type: 'bar',
        data: {
          labels: new_labels,
          datasets: set_data(legends, values)
        },
        options: {
          title: {
            display: true,
            text: 'Population growth (millions)'
          }
        }
})};