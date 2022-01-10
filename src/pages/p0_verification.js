import lock from '../img/lock.svg'

function Verification(props) {
    let {setData} = props

    function verify() {
        let code = document.getElementById('code').value.toLowerCase()
        if (code.length === 6) {
            fetch("https://harrilee.site/wx2022/code", {
                mode: 'cors',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    code: code
                })
            }).then(res => {
                return res.json()
            }).then(d => {
                if (d.success) {
                    document.getElementById('page_0').style.opacity = 0
                    setTimeout(()=>{
                        setData(d.data)
                    },500)
                } else if (d.success === false) {
                    document.getElementById('tips').style.opacity = 0.7
                } else {
                    alert('后端错误，请联系管理员')
                }
            });
        }

    }

    return (
        <div className={'swipe_container'} id={'page_0'}>
            <img src={lock} width={'30%'}/>
            <div>
                <p className={'header'}>
                    本链接涉及用户隐私
                    <br/>
                    请输入验证码以继续
                </p>
            </div>
            <input id={'code'} name={'code'} type={'text'} maxLength={'6'} className={'verify_input'}
                   onChange={verify}/>
            <span className={'tips'} id={'tips'}>密码错误</span>
        </div>
    )
}

export default Verification;