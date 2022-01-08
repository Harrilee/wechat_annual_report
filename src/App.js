import logo from './logo.svg';
import './App.css';

// Import Swiper React components
import { Swiper, SwiperSlide } from "swiper/react";

// Import Swiper styles
import "swiper/css";

// Import slides
import Verification from "./pages/p0_verification";

function App() {

    return (
        <Swiper className="mySwiper" direction={'vertical'} >
            <SwiperSlide><Verification /></SwiperSlide>
            <SwiperSlide>Slide 2</SwiperSlide>
            <SwiperSlide>Slide 3</SwiperSlide>
            <SwiperSlide>Slide 4</SwiperSlide>
            <SwiperSlide>Slide 5</SwiperSlide>
        </Swiper>
    );
}

export default App;
