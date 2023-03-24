data = data.replaceAll('$', ',""~').replaceAll('~', '],[');
data = JSON.parse(data);
data = data.map(p => {
	p.data = p.data.map((d, i) => {
		if (i == 0) {
			return d;
		}
		d[0] += p.data[i - 1][0];
		if (p.data[i - 1][1] !== '') {
			d[1] += p.data[i - 1][1];
		}
		return d;
	});
	p.data = p.data.map((d, i) => {
		d[0] *= 1000;
		return d;
	});
	return p;
});

var dom = document.getElementById('chart-container');
var myChart = echarts.init(dom, 'dark', {
	renderer: 'canvas',
	useDirtyRect: false
});
var app = {};

var option;

option = {
	title: {
		text: ''
	},
	tooltip: {
		trigger: 'axis'
	},
	legend: {
		right: '80px',
		data: data.map(d => d.name),
		selectedMode: 'multiple',
		selected: data.reduce((acc, cur, i) => {
			acc[cur.name] = i < 9;
			return acc;
		})
	},
	grid: {
		left: '3%',
		right: '4%',
		bottom: '5%',
		top: '10%',
		containLabel: true
	},
	toolbox: {
		feature: {
			restore: {},
		}
	},
	xAxis: {
		type: 'time',
		boundaryGap: false
	},
	yAxis: {
		type: 'value',
		maxInterval: 5000
	},
	dataZoom: [
		/*{
			type: 'inside',
			start: data[0].data[0][0],
			end: data[0].data[data[0].data.length - 1][0]
		},
		{
			start: data[0].data[0][0],
			end: data[0].data[data[0].data.length - 1][0]
		}*/
		{
			type: 'slider',
			xAxisIndex: 0,
			filterMode: 'none'
		},
		{
			type: 'slider',
			yAxisIndex: 0,
			filterMode: 'none'
		},
		{
			type: 'inside',
			xAxisIndex: 0,
			filterMode: 'none'
		},
		{
			type: 'inside',
			yAxisIndex: 0,
			filterMode: 'none'
		}
	],
	series: data
};

if (option && typeof option === 'object') {
	myChart.setOption(option);
}

window.addEventListener('resize', myChart.resize);

document.querySelector('#select-all').addEventListener('click', () => {
	myChart.dispatchAction({
		type: 'legendAllSelect'
	});
});
document.querySelector('#select-none').addEventListener('click', () => {
	myChart.dispatchAction({
		type: 'legendAllSelect'
	});
	myChart.dispatchAction({
		type: 'legendInverseSelect',
	});
});