import React from "react";
import Slider from "react-slick";
import styled from "styled-components";
// Components
import TestimonialBox from "../Elements/TestimonialBox";

const testimonials = [ { text: "« J'aime beaucoup les produits Délice pour leur bon goût et leur qualité. Ce sont des produits que je retrouve facilement et que j'apprécie au quotidien. »", author: "Amira B.", role: "Cliente", }, { text: "« Les yaourts Délice sont délicieux et proposent une belle variété de saveurs. Il y a toujours quelque chose qui plaît à toute la famille. »", author: "Sarra M.", role: "Cliente", }, { text: "« J'apprécie les produits Délice pour leur goût et leur praticité. Ils font partie de mes choix habituels pour le petit-déjeuner et les collations. »", author: "Yassine K.", role: "Client", }, { text: "« Ce que j'aime chez Délice, c'est la diversité des produits proposés. On peut choisir parmi différentes options selon ses goûts et ses envies. »", author: "Meriem H.", role: "Cliente", }, { text: "« Délice est une marque que je connais depuis longtemps. J'apprécie de retrouver ses produits facilement dans les commerces près de chez moi. »", author: "Nour E.", role: "Cliente", }, ];

export default function TestimonialSlider() {
  const settings = {
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: false,
    responsive: [
      {
        breakpoint: 900,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };
  return (
    <div>
      <Slider {...settings}>
        {testimonials.map((testimonial) => (
          <LogoWrapper className="flexCenter" key={testimonial.author}>
            <TestimonialBox text={testimonial.text} author={testimonial.author} role={testimonial.role} />
          </LogoWrapper>
        ))}
      </Slider>
    </div>
  );
}

const LogoWrapper = styled.div`
  height: 100%;
  padding: 0 12px;
  cursor: pointer;

  > div {
    height: calc(100% - 30px);
  }

  :focus-visible {
    outline: none;
    border: 0px;
  }
`;
