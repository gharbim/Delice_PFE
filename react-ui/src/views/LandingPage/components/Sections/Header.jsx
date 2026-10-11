import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
// Components
import FullButton from "../Buttons/FullButton";
// Assets - paths updated to new location
import About_deliceImage from "../../../../assets/landing/img/about_delice.jpg";
import Dots from "../../../../assets/landing/svg/Dots";

const easeOut = [0.22, 1, 0.36, 1];

export default function Header() {
  return (
    <Wrapper id="home" className="container flexSpaceCenter">
      <BlobOne />
      <BlobTwo />
      <LeftSide className="flexCenter">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: easeOut }}
        >
          
<Eyebrow className="font13 semiBold">
  Groupe agroalimentaire tunisien
</Eyebrow>

<h1 className="extraBold font60">
  À propos de Délice Holding
</h1>

<HeaderP className="font13 semiBold">
  Délice Holding est un acteur majeur de l'industrie agroalimentaire
  en Tunisie, notamment dans le secteur laitier. À travers ses
  différentes activités, le groupe propose une gamme de produits
  destinés aux consommateurs tunisiens. Engagé dans une démarche
  d'amélioration continue, Délice Holding accorde une importance
  particulière à la qualité de ses produits, à l'innovation et à la
  satisfaction de ses clients.
</HeaderP>

<BtnWrapper>
  <FullButton
    title="Découvrir notre groupe"
    bgColor="#2DCFFF"
    hoverColor="#0FA8D6"
    textColor="#ffffff"
    arrow
  />
</BtnWrapper>
        </motion.div>
      </LeftSide>
      <RightSide>
        <motion.div
          initial={{ opacity: 0, y: 24, scale: 0.96 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.15, ease: easeOut }}
          style={{ position: "relative", zIndex: 9 }}
        >
          <ImageWrapper>
            <Img className="radius8" src={About_deliceImage} alt="office" style={{ width: "420px", height: "auto", zIndex: 9 }} />
            <DotsWrapper>
              <Dots />
            </DotsWrapper>
          </ImageWrapper>
        </motion.div>
        <GreyDiv className="lightBg"></GreyDiv>
      </RightSide>
    </Wrapper>
  );
}

const Wrapper = styled.section`
  padding-top: 80px;
  width: 100%;
  min-height: 840px;
  position: relative;
  @media (max-width: 960px) {
    flex-direction: column;
  }
`;
const Eyebrow = styled.h4`
  display: inline-block;
  color: #2dcfff;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 14px;
`;
const BlobOne = styled.div`
  position: absolute;
  top: -60px;
  left: -120px;
  width: 380px;
  height: 380px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(45, 207, 255, 0.22) 0%, rgba(45, 207, 255, 0) 70%);
  z-index: 0;
  pointer-events: none;
`;
const BlobTwo = styled.div`
  position: absolute;
  top: 260px;
  right: 60px;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(252, 153, 15, 0.14) 0%, rgba(252, 153, 15, 0) 70%);
  z-index: 0;
  pointer-events: none;
  @media (max-width: 960px) {
    display: none;
  }
`;
const LeftSide = styled.div`
  width: 50%;
  height: 100%;
  @media (max-width: 960px) {
    width: 100%;
    order: 2;
    margin: 50px 0;
    text-align: center;
  }
  @media (max-width: 560px) {
    margin: 80px 0 50px 0;
  }
`;
const RightSide = styled.div`
  width: 50%;
  height: 100%;
  @media (max-width: 960px) {
    width: 100%;
    order: 1;
    margin-top: 30px;
  }
`;
const HeaderP = styled.div`
  max-width: 470px;
  padding: 15px 0 50px 0;
  line-height: 1.5rem;
  @media (max-width: 960px) {
    padding: 15px 0 50px 0;
    text-align: center;
    max-width: 100%;
  }
`;
const BtnWrapper = styled.div`
  max-width: 190px;
  @media (max-width: 960px) {
    margin: 0 auto;
  }
`;
const GreyDiv = styled.div`
  width: 30%;
  height: 700px;
  position: absolute;
  top: 0;
  right: 0;
  z-index: 0;
  @media (max-width: 960px) {
    display: none;
  }
`;
const ImageWrapper = styled.div`
  display: flex;
  justify-content: flex-end;
  position: relative;
  z-index: 9;
  @media (max-width: 960px) {
    width: 100%;
    justify-content: center;
  }
`;
const Img = styled.img`
  @media (max-width: 560px) {
    width: 80%;
    height: auto;
  }
`;
const DotsWrapper = styled.div`
  position: absolute;
  right: -100px;
  bottom: 100px;
  z-index: 2;
  @media (max-width: 960px) {
    right: 100px;
  }
  @media (max-width: 560px) {
    display: none;
  }
`;
