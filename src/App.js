import './App.css';
import React from 'react';
// Import Swiper React components
import {Swiper, SwiperSlide} from "swiper/react";
// import "swiper/css";
// Import slides
import Verification from "./pages/p0_verification";
import Begin from "./pages/p1_begin";
import Total from "./pages/p2_total"
import MaxDay from "./pages/p3_max_day"
import MaxNight from "./pages/p4_max_night";
import Frequent from "./pages/p5_frequent";
import End from './pages/p6_end'

import Highcharts from 'highcharts'

import config from "./config";

import musicLogo from './img/music.svg'
import texture from './img/texture.jpg'


// import Swiper core and required modules
import SwiperCore, {
    Pagination
} from 'swiper';

// image preload
import lock from './img/lock.svg'
import fu from './img/fu.gif'
import avatar from './img/avatar.jpg'
import fireworks from "./img/fireworks.gif";
import nianhuo from './img/nianhuo.gif'
import jishi from './img/jishi.gif'
import lanten from './img/lanten.gif'
import yanhua from "./img/yanhua.gif";
import tiger from "./img/tiger.gif";
import xinchunhaonian from './img/xinchunhaonian.gif'
import fishes from './img/fishes.gif'

const preload_img_list = [lock, fu, avatar, fireworks, nianhuo, jishi, lanten, yanhua, tiger,
    musicLogo, texture, xinchunhaonian, fishes]

// install Swiper modules
SwiperCore.use([Pagination]);

const is_phone = navigator.userAgent.indexOf('iPhone') !== -1 || navigator.userAgent.indexOf('Android') !== -1 || navigator.userAgent.indexOf('iPad') !== -1

Highcharts.setOptions({
    lang: {
        contextButtonTitle: "图表导出菜单",
        decimalPoint: ".",
        downloadJPEG: "下载JPEG图片",
        downloadPDF: "下载PDF文件",
        downloadPNG: "下载PNG文件",
        downloadSVG: "下载SVG文件",
        drillUpText: "返回 {series.name}",
        loading: "加载中",
        months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
        noData: "没有数据",
        numericSymbols: ["千", "兆", "G", "T", "P", "E"],
        printChart: "打印图表",
        resetZoom: "恢复缩放",
        resetZoomTitle: "恢复图表",
        shortMonths: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
        thousandsSep: ",",
        weekdays: ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
    },
})

function MusicLogo() {
    const [play, setPlay] = React.useState(true)
    return (
        <img src={musicLogo} className={play ? 'music_rotate' : 'music'} alt={'music logo'} onClick={() => {
            if (play) {
                document.getElementById('bgAudio').pause();
            } else {
                document.getElementById('bgAudio').play();
            }
            setPlay(!play);
        }}/>
    )
}

function BgAudio() {
    return (
        <audio muted autoPlay id={'bgAudio'} loop>
            <source
                src={config.bgAudio.src1_url}
                type={config.bgAudio.src1_type}/>
            <source src={config.bgAudio.src2_url} type={config.bgAudio.src2_type}/>
            Your browser does not support the audio element.
        </audio>
    )
}

function App() {
    let [data, setData] = React.useState(null)
    React.useEffect(() => {
        if (is_phone) {
            document.getElementById("bgAudio").muted = false;
            document.getElementById("bgAudio").muted = true;
            if (data && document.getElementById("bgAudio")) {
                document.getElementById("bgAudio").muted = false;
            }
            // image preload
            preload_img_list.forEach(url => {
                var img = new Image()
                img.src = url
                img.hidden = true
                document.body.appendChild(img)
            })
        }

    })
    console.log(navigator.userAgent)
    if (!is_phone) {
        return (
            <div className={'mySwiper'} style={{backgroundImage: `url(${texture})`, backgroundSize: "cover"}}>
                <div className={'UA_constraint'}>
                    <p>
                        请使用手机浏览器查看此页面
                    </p>
                    <p>
                        推荐使用微信打开此页面
                    </p>
                </div>
            </div>
        )
    }
    if (!data) {
        return (
            <div className={'mySwiper'} style={{backgroundImage: `url(${texture})`, backgroundSize: "cover"}}>
                <Verification setData={setData}/>
                <BgAudio/>
            </div>
        )
    }
    return (
        <>
            <BgAudio/>
            <MusicLogo/>
            <Swiper className="mySwiper" direction={'vertical'} pagination={{
                "clickable": true,
            }} style={{backgroundImage: `url(${texture})`, backgroundSize: "cover"}}>
                <SwiperSlide><Begin data={data}/></SwiperSlide>
                <SwiperSlide><Total data={data}/></SwiperSlide>
                <SwiperSlide><MaxDay data={data}/></SwiperSlide>
                <SwiperSlide><MaxNight data={data}/></SwiperSlide>
                <SwiperSlide><Frequent data={data}/></SwiperSlide>
                <SwiperSlide><End data={data}/></SwiperSlide>
            </Swiper>
        </>

    );
}

export default App;
