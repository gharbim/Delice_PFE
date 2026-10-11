import React from "react";
import styled from "styled-components";
// Components
import ClientSlider from "../Elements/ClientSlider";
import ServiceBox from "../Elements/ServiceBox";
import FullButton from "../Buttons/FullButton";
import Reveal from "../Elements/Reveal";
// Assets
import AddImage1 from "../../../../assets/landing/img/add/1.png";
import AddImage2 from "../../../../assets/landing/img/add/2.png";
import AddImage3 from "../../../../assets/landing/img/add/3.png";
import AddImage4 from "../../../../assets/landing/img/add/4.png";

export default function Services() {
  return (
    <Wrapper id="services">
      <div className="lightBg" style={{ padding: "50px 0" }}>
        <div className="container">
          <ClientSlider />
        </div>
      </div>

      <div className="whiteBg" style={{ padding: "60px 0" }}>
        <div className="container">
          <Reveal>
            <HeaderInfo>
              <h1 className="font40 extraBold">Nos services</h1>
            </HeaderInfo>
          </Reveal>

 
        <ServiceBoxRow>
          <Reveal delay={0} style={{ flex: 1, display: "flex" }}>
            <ServiceBoxWrapper>
              <ServiceBox
                icon="roller"
                title="Produits laitiers"
                subtitle="Délice propose une gamme de produits laitiers comprenant du lait, des yaourts et d'autres produits dérivés, adaptés aux besoins des consommateurs."
              />
            </ServiceBoxWrapper>
          </Reveal>

          <Reveal delay={0.08} style={{ flex: 1, display: "flex" }}>
            <ServiceBoxWrapper>
              <ServiceBox
                icon="monitor"
                title="Production agroalimentaire"
                subtitle="Le groupe s'appuie sur son savoir-faire industriel pour transformer le lait et produire des aliments répondant aux attentes du marché."
              />
            </ServiceBoxWrapper>
          </Reveal>

          <Reveal delay={0.16} style={{ flex: 1, display: "flex" }}>
            <ServiceBoxWrapper>
              <ServiceBox
                icon="browser"
                title="Qualité et sécurité alimentaire"
                subtitle="Délice accorde une importance particulière à la qualité des produits, aux processus de fabrication et au respect des exigences de sécurité alimentaire."
              />
            </ServiceBoxWrapper>
          </Reveal>

          <Reveal delay={0.24} style={{ flex: 1, display: "flex" }}>
            <ServiceBoxWrapper>
              <ServiceBox
                icon="printer"
                title="Distribution et proximité"
                subtitle="Grâce à son réseau de distribution, le groupe assure la disponibilité de ses produits auprès des points de vente et des consommateurs en Tunisie."
              />
            </ServiceBoxWrapper>
          </Reveal>
        </ServiceBoxRow>


        </div>

        {/* ===== Advertising section (unchanged) ===== */}
        <div className="lightBg">
          {/* <div className="container">
            <Advertising className="flexSpaceCenter">
              <AddLeft>
                <h4 className="font15 semiBold">A few words about company</h4>
                <h2 className="font40 extraBold">A Study of Creativity</h2>
                <p className="font12">
                  Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat.
                </p>

                <ButtonsRow>
                  <div style={{ width: "190px" }}>
                    <FullButton title="Get Started" action={() => alert("clicked")} />
                  </div>
                  <div style={{ width: "190px", marginLeft: "15px" }}>
                    <FullButton title="Contact Us" action={() => alert("clicked")} border />
                  </div>
                </ButtonsRow>
              </AddLeft>

              <AddRight>
                <AddRightInner>
                  <div className="flexNullCenter">
                    <AddImgWrapp1><img src={AddImage1} alt="office" /></AddImgWrapp1>
                    <AddImgWrapp2><img src={AddImage2} alt="office" /></AddImgWrapp2>
                  </div>
                  <div className="flexNullCenter">
                    <AddImgWrapp3><img src={AddImage3} alt="office" /></AddImgWrapp3>
                    <AddImgWrapp4><img src={AddImage4} alt="office" /></AddImgWrapp4>
                  </div>
                </AddRightInner>
              </AddRight>
            </Advertising>
          </div> */}
        </div>
      </div>
    </Wrapper>
  );
}

/* =======================
   ✅ FIXED STYLES (IMPORTANT PART)
======================= */

const Wrapper = styled.section`
  width: 100%;
`;

/* 🔥 KEY FIX: equal height alignment */
const ServiceBoxRow = styled.div`
  display: flex;
  align-items: stretch;
  gap: 30px;

  @media (max-width: 860px) {
    flex-direction: column;
  }
`;

const ServiceBoxWrapper = styled.div`
  flex: 1;
  display: flex;
`;

/* optional but helps spacing consistency */
const HeaderInfo = styled.div`
  @media (max-width: 860px) {
    text-align: center;
  }
`;

const Advertising = styled.div`
  margin: 80px 0;
  padding: 100px 0;
  position: relative;

  @media (max-width: 860px) {
    flex-direction: column;
    padding: 0;
  }
`;

const ButtonsRow = styled.div`
  display: flex;
  margin: 30px 0;

  @media (max-width: 860px) {
    justify-content: space-between;
  }
`;

const AddLeft = styled.div`
  width: 50%;
`;

const AddRight = styled.div`
  width: 50%;
  position: absolute;
  top: -70px;
  right: 0;

  @media (max-width: 860px) {
    position: relative;
    width: 100%;
  }
`;

const AddRightInner = styled.div`
  width: 100%;
`;

const AddImgWrapp1 = styled.div`
  width: 48%;
  margin: 0 6% 10px 6%;
  img { width: 100%; border-radius: 1rem; }
`;

const AddImgWrapp2 = styled.div`
  width: 30%;
  margin: 0 5% 10px 5%;
  img { width: 100%; border-radius: 1rem; }
`;

const AddImgWrapp3 = styled.div`
  width: 20%;
  margin-left: 40%;
  img { width: 100%; border-radius: 1rem; }
`;

const AddImgWrapp4 = styled.div`
  width: 30%;
  margin: 0 5% auto;
  img { width: 100%; border-radius: 1rem; }
`;