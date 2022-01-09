import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import yanhua from "../img/yanhua.svg";
import tiger from "../img/tiger.png";
function Frequent(props) {
    const {data} = props;
    const options_time = {

        chart: {
            type: 'column',
            width: window.innerWidth * 0.9,
            height: window.innerHeight * 0.3,
            backgroundColor: 'transparent',
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'datetime',
            labels: {
                style:{
                    color: '#ddbfbf'
                },
                formatter: function() {
                    return Highcharts.dateFormat('%H点', this.value);
                }
            },
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: '聊天总数'
            },
            labels: {
                formatter: function () {
                    return this.value / 1000 + 'k';
                }
            },
            visible: false,

        },
        tooltip: {
            pointFormat: '{series.name}：<b>{point.y}</b>',
            xDateFormat:'%H点',
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            column: {
                borderWidth: 0
            }
        },
        series: [{
            name: '收发总数',
            data: data.data.timeCount,
            pointStart: Date.UTC(2022, 0, 3,0,0,0),
            pointInterval: 36e5,
        }],
        colors: ['#fab129', '#ddbfbf'],
        credits: {
            enabled: false
        },

    }
    const options_week = {
        chart: {
            type: 'column',
            width: window.innerWidth * 0.9,
            height: window.innerHeight * 0.3,
            backgroundColor: 'transparent',
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'datetime',
            labels: {
                style:{
                    color: '#ddbfbf'
                },
                tickInterval:24*36e5,
                formatter: function() {
                    return Highcharts.dateFormat('%a', this.value);
                }
            },
            showLastLabel: true,
            step: 24*36e5
        },
        yAxis: {
            title: {
                text: '聊天总数'
            },
            labels: {
                formatter: function () {
                    return this.value / 1000 + 'k';
                }
            },
            visible: false,

        },
        tooltip: {
            pointFormat: '{series.name}：<b>{point.y}</b>',
            xDateFormat:'%a',
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            column: {
                borderWidth: 0
            }
        },
        series: [{
            name: '收发总数',
            data: data.data.weekCount,
            pointStart: Date.UTC(2022, 0, 2,0,0,0),
            pointInterval: 24*36e5,
        }],
        colors: ['#fab129', '#ddbfbf'],
        credits: {
            enabled: false
        },

    }
    return <div className={'swipe_container_left'}>
        <img src={yanhua} width={"100%"} style={{position: 'absolute', top:0, right:0}}/>
        <img src={tiger} width={"100%"} style={{position: 'absolute', bottom:0, right:0}}/>
        <p>我们习惯在
            <span className={'keywords'}>{data.stats.frequent.start}</span>
            至
            <span className={'keywords'}>{data.stats.frequent.end}</span>
            聊天
        </p>
        <HighchartsReact class={"chart"}
                         highcharts={Highcharts}
                         options={options_time}
        />
        <p>
            一周7天里，
            <br />
            <span className={'keywords'}>{data.stats.frequent.weekday}</span>
            是我们聊天最频繁的日子
        </p>
        <HighchartsReact class={"chart"}
                         highcharts={Highcharts}
                         options={options_week}
        />
    </div>
}

export default Frequent;