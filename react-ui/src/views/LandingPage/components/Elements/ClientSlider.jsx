import React from "react";
import Slider from "react-slick";
import styled from "styled-components";

// Assets
import ClientLogo01 from "../../../../assets/landing/img/clients/delice_milkana.png";
import ClientLogo02 from "../../../../assets/landing/img/clients/delice_fruit.png";
import ClientLogo03 from "../../../../assets/landing/img/clients/delice.jpg";
import ClientLogo04 from "../../../../assets/landing/img/clients/dlice_danone.jpg";
// import ClientLogo05 from "../../../../assets/landing/img/clients/Microsoft-Azure-Logo.png";
// import ClientLogo06 from "../../../../assets/landing/img/clients/Fivetran.png";
// import ClientLogo07 from "../../../../assets/landing/img/clients/Anaplan_logo.png";
// import ClientLogo08 from "../../../../assets/landing/img/clients/dataiku_logo.png";
// import ClientLogo09 from "../../../../assets/landing/img/clients/microsoft_logo.png";
// import ClientLogo10 from "../../../../assets/landing/img/clients/Qlik_Logo.png";

export default function ClientSlider() {
  const settings = {
    infinite: true,
    speed: 500,
    slidesToShow: 6,
    slidesToScroll: 2,
    arrows: false,
    autoplay: true,
    autoplaySpeed: 2500,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 4,
          slidesToScroll: 2,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
        },
      },
    ],
  };

  const logos = [
    ClientLogo01,
    ClientLogo02,
    ClientLogo03,
    ClientLogo04
  ];

  return (
    <Slider {...settings}>
      {logos.map((logo, index) => (
        <LogoWrapper key={index}>
          <ImgStyle src={logo} alt={`Client ${index + 1}`} />
        </LogoWrapper>
      ))}
    </Slider>
  );
}

const LogoWrapper = styled.div`
  height: 120px;
  display: flex !important;
  justify-content: center;
  align-items: center;
  padding: 15px;
  box-sizing: border-box;
`;

const ImgStyle = styled.img`
  width: 170px;
  height: 70px;
  object-fit: contain;
  display: block;
`;