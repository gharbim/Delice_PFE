import React from "react";
import styled from "styled-components";
// Components
import ProjectBox from "../Elements/ProjectBox";
import FullButton from "../Buttons/FullButton";
import Reveal from "../Elements/Reveal";
// Assets
import ProjectImg1 from "../../../../assets/landing/img/projects/1.png";
import ProjectImg2 from "../../../../assets/landing/img/projects/2.png";
import ProjectImg3 from "../../../../assets/landing/img/projects/3.png";
import ProjectImg4 from "../../../../assets/landing/img/projects/4.png";
import ProjectImg5 from "../../../../assets/landing/img/projects/5.png";
import ProjectImg6 from "../../../../assets/landing/img/projects/6.png";
import AddImage2 from "../../../../assets/landing/img/add/add2.png";

export default function Projects() {
  return (
    <Wrapper id="projects">
      <div className="whiteBg">
        <div className="container">
          <Reveal>
            <HeaderInfo>
              <h1 className="font40 extraBold">
                Les atouts de Délice Holding
              </h1>
            </HeaderInfo>
          </Reveal>

          <div className="row textCenter">
            <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4">
              <Reveal delay={0}>
                <ProjectBox
                  img={ProjectImg1}
                  title="Des produits de qualité"
                  text="Une attention particulière portée à la qualité et à la sécurité alimentaire, de la production jusqu'au consommateur."
                  action={() => alert("clicked")}
                />
              </Reveal>
            </div>

            <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4">
              <Reveal delay={0.1}>
                <ProjectBox
                  img={ProjectImg2}
                  title="L'innovation au quotidien"
                  text="Une démarche d'amélioration continue pour développer des produits adaptés aux besoins et aux attentes des consommateurs."
                  action={() => alert("clicked")}
                />
              </Reveal>
            </div>

            <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4">
              <Reveal delay={0.2}>
                <ProjectBox
                  img={ProjectImg3}
                  title="Une présence de proximité"
                  text="Un réseau de distribution qui contribue à rendre les produits du groupe accessibles aux consommateurs à travers la Tunisie."
                  action={() => alert("clicked")}
                />
              </Reveal>
            </div>
          </div>
        </div>
      </div>
    </Wrapper>
  );
}

const Wrapper = styled.section`
  width: 100%;
`;

const HeaderInfo = styled.div`
  padding: 70px 0 30px 0;

  @media (max-width: 860px) {
    text-align: center;
  }
`;

const Advertising = styled.div`
  padding: 100px 0;
  margin: 100px 0;
  position: relative;

  @media (max-width: 1160px) {
    padding: 60px 0 40px 0;
  }

  @media (max-width: 860px) {
    flex-direction: column;
    padding: 0 0 30px 0;
    margin: 80px 0 0px 0;
  }
`;

const ButtonsRow = styled.div`
  @media (max-width: 860px) {
    justify-content: space-between;
  }
`;

const AddLeft = styled.div`
  position: relative;
  width: 50%;

  p {
    max-width: 475px;
  }

  @media (max-width: 860px) {
    width: 80%;
    order: 2;
    text-align: center;

    h2 {
      line-height: 3rem;
      margin: 15px 0;
    }

    p {
      margin: 0 auto;
    }
  }
`;

const AddRight = styled.div`
  width: 50%;

  @media (max-width: 860px) {
    width: 80%;
    order: 2;
  }
`;

const AddLeftInner = styled.div`
  width: 100%;
  position: absolute;
  top: -300px;
  left: 0;

  @media (max-width: 1190px) {
    top: -250px;
  }

  @media (max-width: 920px) {
    top: -200px;
  }

  @media (max-width: 860px) {
    order: 1;
    position: relative;
    top: -60px;
    left: 0;
  }
`;

const ImgWrapper = styled.div`
  width: 100%;
  padding: 0 15%;

  img {
    width: 100%;
    height: auto;
  }

  @media (max-width: 400px) {
    padding: 0;
  }
`;