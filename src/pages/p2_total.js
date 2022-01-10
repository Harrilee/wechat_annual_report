import fireworks from "../img/fireworks.gif";
import * as moment from 'moment';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'

function Total(props) {
    const {data} = props;
    const first_day = moment(new Date(data.stats.earlist.year,data.stats.earlist.month-1,data.stats.earlist.day))
    const last_days = moment().diff(first_day, 'd')
    console.log(first_day)
    const options = {
        chart: {
            type: 'area',
            width: window.innerWidth * 0.9,
            height: window.innerHeight * 0.3,
            backgroundColor: 'transparent'
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
                }
            },
            formatter: function() {
                return Highcharts.dateFormat('%m', this.value);
            }
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
            pointFormat: '{series.name}：<b>{point.y}</b>'
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                pointStart: 2021,
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                },
            }
        },
        series: [{
            name: '收发总数',
            data: data.data.chatCount,
            pointStart: Date.UTC(2021, 0, 1),
            pointInterval: 24 * 36e5,
        }],
        colors: ['#fab129', '#ddbfbf'],
        credits: {
            enabled: false
        },

    }

    return <div className={'swipe_container_left'}>
        <img src={fireworks} width={"20%"} style={{position: 'absolute', top:0, right:10}}/>
        <p>
            {`我们相识于`}<span
            className={'keywords'}>{`${data.stats.earlist.year}年${data.stats.earlist.month}月${data.stats.earlist.day}日`}</span>{`*，`}
            <br/>
            <span className={'keywords'}>{`${last_days}天`}</span>{`的日日夜夜，`}
            <br/>
            {`记录着彼此的点点滴滴；`}
        </p>
        <p>
            {`2021年，`}
            <br/>
            {`我们总共收发了`}<span className={'keywords'}>{`${data.stats.total.msg}条`}</span>{`消息；`}
            <br/>
        </p>
        <p>
            <span className={'keywords'}>{`${data.stats.contin.startMonth}月${data.stats.contin.startDay}日`}</span>
            至
            <span className={'keywords'}>{`${data.stats.contin.endMonth}月${data.stats.contin.endDay}日`}</span>
            <br/>
            {`我们连续聊了`}<span className={'keywords'}>{`${data.stats.contin.days}天`}</span>{`，`}
            <br/>
            是今年连续聊天最长的一段时间。
        </p>
        <HighchartsReact class={"chart"}
                         highcharts={Highcharts}
                         options={options}
        />
        <p className={'consent'} style={{margin: 'auto', marginTop:0, marginBottom:0}}>点击图表浏览详细数据</p>
        <br/>
        <p className={'consent'}>* 该数据取自微信聊天记录数据库中最早一条的时间，全部数据库中最早记录约为2019年6月。</p>
    </div>
}

export default Total;