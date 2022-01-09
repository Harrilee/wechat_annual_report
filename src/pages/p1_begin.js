import fu from '../img/fu.svg'

function Begin(props) {
    const {data} = props
    return (
        <div className={'swipe_container'}>
            <img src={fu} width={'40%'}/>
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