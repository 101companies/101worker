# Templates

All files contained in this folder are used by the visualizer.


## googleChart

With these googleCharts templates you can quickly create simple or even highly customized charts.

To use the visualization you need to add the folling parameter to your config.json: 
* visualization = true
To do so simply use the following function in your visualization.py:
* env.create_googleChart(chartType, chartName, data, options)

chartType		defines the template to use for creating a chart
chartName		defines a custom name for the chart and although the name of the chart in the index file
data			defines the resouces used for chart creation, for further documentation see below
options			defines the options used for chart creation, those can be customly specified


## documentation
For a full documentation of google charts please refer to the general documentation.
*https://developers.google.com/chart/interactive/docs/

For usig the templates here is a general example how data and options could look like.
* sample data
data = [
	['Language', 'Speakers (in millions)'],
	['German',  5.85],
	['French',  1.66]
	]);
* sample options
options = {
	legend: 'none',
	pieSliceText: 'label',
	title: 'Swiss Language Use (100 degree rotation)',
	pieStartAngle: 100,
    };

### google pie chart
* chartType	'pieChart'
* chartName	String customŃame
* data		refer to https://developers.google.com/chart/interactive/docs/gallery/piechart#data-format
* options	refer to https://developers.google.com/chart/interactive/docs/gallery/piechart#configuration-options

### google bar chart
* chartType	'pieChart'
* chartName	String customŃame
* data		refer to https://developers.google.com/chart/interactive/docs/gallery/barchart#data-format
* options	refer to https://developers.google.com/chart/interactive/docs/gallery/barchart#configuration-options

### google line chart
* chartType	'pieChart'
* chartName	String customŃame
* data		refer to https://developers.google.com/chart/interactive/docs/gallery/linechart#data-format
* options	refer to https://developers.google.com/chart/interactive/docs/gallery/linechart#configuration-options

### google bubble chart
* chartType	'pieChart'
* chartName	String customŃame
* data		refer to https://developers.google.com/chart/interactive/docs/gallery/bubblechart#data-format
* options	refer to https://developers.google.com/chart/interactive/docs/gallery/bubblechart#configuration-options
