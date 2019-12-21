
function buildCharts(factor) {
  d3.json(`/factors/${factor}`).then((data) => {
    const runtimes = data.runtimes;
    const profits = data.profits;
    const budgets = data.budgets;
    const ratings = data.ratings;
    const titles = data.titles;
    const genres = data.genres;
    const revenues = data.revenues;

    // Build a Bubble Chart
    var bubbleLayout = {
      margin: { t: 0 },
      hovermode: "closest",
      xaxis: { title: "factor" }
    };
    var bubbleData = [
      {
        x: factor,
        y: profits,
        text: titles,
        mode: "markers",
        marker: {
          size: revenues,
          color: genres,
          colorscale: "Earth"
        },
        hovertemplate:
        "<b>%{text}</b><br><br>" +
        "%{yaxis.title.text}: %{y:$,.0f}<br>" +
        "%{xaxis.title.text}: %{x:$,.0f}<br>" +
        "<extra></extra>"
      }
    ];

    Plotly.plot("bubble", bubbleData, bubbleLayout);

    // Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
    var barData = [
      {
        x: factor,
        y: profits
      }
    ];

    var barLayout = {
      autosize: true,
      xaxis: {
        automargin: true
      }
    };

    Plotly.plot("bar", barData, barLayout);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/factor").then((factorNames) => {
    factorNames.forEach((factor) => {
      selector
        .append("option")
        .text(factor)
        .property("value", factor);
    });

    // Use the first sample from the list to build the initial plots
    const firstFactor = factorNames[0];
    buildCharts(firstFactor);
    buildMetadata(firstFactor);
  });
}

function optionChanged(newFactor) {
  // Fetch new data each time a new sample is selected
  buildCharts(newFactor);
}

// Initialize the dashboard
init();
