import fishes from '../img/fishes.png'
import nianhuo from '../img/nianhuo.png'

function MaxDay(props) {
    const {data} = props;

    return <div className={'swipe_container_left_top'}>
        <img src={fishes} width={"100%"} style={{position: 'absolute', top:0, right:0}}/>
        <img src={nianhuo} width={"100%"} style={{position: 'absolute', bottom:0, right:0}}/>
        <p>
            <span
            className={'keywords'}>{`${data.stats.max.month}月${data.stats.max.day}日`}</span>{`，`}
            <br/>
            {`我们收发消息共`}<span className={'keywords'}>{`${data.stats.max.msgs}条`}</span>{`，`}
            <br/>
            {`为2021年最多的一天；`}
        </p>
        <div style={{width:"100%"}}>
            {`那天我们的关键词是：`}
            <p className={'keywords_group'}>
                <span className={'keywords'}>{`${data.stats.max.key1}`}</span>
                <br/>
                <span className={'keywords'}>{`${data.stats.max.key2}`}</span>
                <br/>
                <span className={'keywords'}>{`${data.stats.max.key3}`}</span>
            </p>

        </div>
        <p>
            {data.par.maxDay}
        </p>
    </div>
}

export default MaxDay;