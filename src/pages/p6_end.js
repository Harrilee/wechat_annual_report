import xinchunhaonian from '../img/xinchunhaonian.png'


function End(props) {
    const {data} = props;

    return <div className={'swipe_container_left_bottom'}>
        <img src={xinchunhaonian} width={"100%"} style={{position: 'absolute', top:0, right:0}}/>
        <p>
            2021年，
            <br />
            我们的年度10大关键词是
        </p>
        <div style={{width:"100%"}}>
            <p className={'keywords_group_all'}>
                <span className={'keywords_all'}>{`${data.stats.total.key0}`}</span>
                <span className={'keywords_all'}>{`${data.stats.total.key1}`}</span>
                <span className={'keywords_all'}>{`${data.stats.total.key2}`}</span>
                <span className={'keywords_all'}>{`${data.stats.total.key3}`}</span>
                <span className={'keywords_all'}>{`${data.stats.total.key4}`}</span>
                <span className={'keywords_all'}>{`${data.stats.total.key5}`}</span>
                <span className={'keywords_all'}>{`${data.stats.total.key6}`}</span>
                <span className={'keywords_all'}>{`${data.stats.total.key7}`}</span>
                <span className={'keywords_all'}>{`${data.stats.total.key8}`}</span>
                <span className={'keywords_all'}>{`${data.stats.total.key9}`}</span>
            </p>

        </div>
        <p>
            {data.user.par.end}
        </p>
        <br/><br/>
    </div>
}

export default End;