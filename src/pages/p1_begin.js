import fu from '../img/fu.svg'

function Begin(props) {
    const {data} = props
    return (
        <div className={'swipe_container'}>
            <img src={fu} width={'40%'}/>
            <div className={"avatar_container"}>
                <div className={'avatar'} style={{backgroundImage: `url(${data.my.avatar})`, transform:`translateX(7px)`, zIndex:3}} />
                <div className={'avatar'} style={{backgroundImage: `url(${data.user.avatar})`, transform:`translateX(-7px)`}}/>
            </div>
            <br />
            <div>
                <p>{data.user.username+'您好，'}</p>
                <p>{data.par.intro}</p>
            </div>
            <br/>
            <br/>
            <br/>
            <div className={'button'} onClick={()=>{document.getElementsByClassName("swiper-pagination-bullet")[1].click()}}>
                开启我们的2021
            </div>
            <br/>
            <p className={'consent'}>{data.par.legal_info}</p>
        </div>
    )
}

export default Begin;