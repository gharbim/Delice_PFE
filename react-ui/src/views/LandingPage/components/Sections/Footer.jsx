import React from "react";
import styled from "styled-components";
import { Link } from "react-scroll";
// Assets - paths updated to new location
import LogoImg from "../../../../assets/landing/svg/Logo";
import KeyrusLogo from "../../../../assets/images/keyrus_logo.png";

export default function Footer() {
  const getCurrentYear = () => {
    return new Date().getFullYear();
  };

  return (
    <Wrapper style={{ borderTop: "1px solid var(--lp-border)" }}>
      <div style={{ backgroundColor: "var(--lp-border)" }}>
        <div className="container">
          <InnerWrapper className="flexSpaceCenter" style={{ padding: "30px 0" }}>
            <FooterLeft>
              <Link className="flexCenter animate pointer" to="home" smooth={true} offset={-80}>
                <img src={KeyrusLogo} alt="Keyrus" style={{ width: "140px", height: "auto" }} />
              </Link>
              <StyleP className="font13 greyColor">
                © {getCurrentYear()} delice. Tous droits réservés.
              </StyleP>
            </FooterLeft>

            <FooterNav className="flexNullCenter">
              <Link className="darkColor animate pointer font13 semiBold" to="services" smooth={true} offset={-80}>
                Services
              </Link>
              <Link className="darkColor animate pointer font13 semiBold" to="contact" smooth={true} offset={-80}>
                Contact
              </Link>
              <Link className="darkColor animate pointer font13 semiBold" to="home" smooth={true} offset={-80}>
                Retour en haut
              </Link>
            </FooterNav>
          </InnerWrapper>
        </div>
      </div>
    </Wrapper>
  );
}

const Wrapper = styled.div`
  width: 100%;
`;

const InnerWrapper = styled.div`
  @media (max-width: 550px) {
    flex-direction: column;
  }
`;

const FooterLeft = styled.div`
  @media (max-width: 550px) {
    text-align: center;
    margin-bottom: 20px;
  }
`;

const FooterNav = styled.div`
  gap: 30px;

  @media (max-width: 550px) {
    gap: 16px;
  }
`;

const StyleP = styled.p`
  margin: 8px 0 0 0;

  @media (max-width: 550px) {
    margin: 8px 0 20px 0;
  }
`;