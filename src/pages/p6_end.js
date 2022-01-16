import xinchunhaonian from '../img/xinchunhaonian.gif'


function End(props) {
    const {data} = props;

    return <div className={'swipe_container_left_bottom'}>
        <img src={xinchunhaonian} width={"100%"} style={{position: 'absolute', top: 0, right: 0}}/>
        <div style={{minHeight: window.innerHeight - window.innerWidth}} className={'center_container'}>
            <p>
                2021年，
                <br/>
                我们的年度关键词是
            </p>
            <div style={{width: "100%"}}>
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
                    <span className={'keywords_all'}>{`${data.stats.total.key10}`}</span>
                    <span className={'keywords_all'}>{`${data.stats.total.key11}`}</span>
                    <span className={'keywords_all'}>{`${data.stats.total.key12}`}</span>
                    <span className={'keywords_all'}>{`${data.stats.total.key13}`}</span>
                    <span className={'keywords_all'}>{`${data.stats.total.key14}`}</span>
                </p>
            </div>
            <div>
                {
                    data.user.par.end.split('\n').map((e, i) => {
                        return <p key={i}>{e}</p>
                    })
                }
            </div>
        </div>
        <br/>
        <p className={'consent'}>
            作者GitHub@Harrilee，代码转送门👉
            <a href={"https://github.com/Harrilee/wechat_annual_report"}>GitHub repo</a>
        </p>
    </div>
}

export default End;