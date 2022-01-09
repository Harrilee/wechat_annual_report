import jishi from '../img/jishi.png'
import lanten from '../img/lanten.svg'
function MaxNight(props) {
    const {data} = props;

    return <div className={'swipe_container_left'}>
        <img src={lanten} width={"100%"} style={{position: 'absolute', top:0, right:0}}/>
        <img src={jishi} width={"100%"} style={{position: 'absolute', bottom:0, right:0}}/>
        <p>
            <span className={'keywords'}>{`${data.stats.latest.month}月${data.stats.latest.day}日`}</span>，
            {+data.stats.latest.mmss.slice(0, 2) < 6 ? "凌晨" :
                +data.stats.latest.mmss.slice(0, 2) < 12 ? "上午" :
                    +data.stats.latest.mmss.slice(0, 2) < 18 ? "下午" : "晚上"}
            <span className={'keywords'}>{data.stats.latest.mmss}</span>*
            <br/>
            {`我们仍在聊天，`}
            <br/>
            {`为2021年最多的一天；`}
        </p>
        <div style={{width:"100%"}}>
            {`那天我们的关键词是：`}
            <p className={'keywords_group'}>
                <span className={'keywords'}>{`${data.stats.latest.key1}`}</span>
                <br/>
                <span className={'keywords'}>{`${data.stats.latest.key2}`}</span>
                <br/>
                <span className={'keywords'}>{`${data.stats.latest.key3}`}</span>
            </p>

        </div>
        <p>
            {data.par.latest}
        </p>
        <br/><br/>
        <p className={'consent'}>* 该数据基于北京时间，”聊天“定义为，双方在5分钟内有互相发送过消息</p>
    </div>
}

export default MaxNight;