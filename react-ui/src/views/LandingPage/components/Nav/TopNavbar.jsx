import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { Link } from "react-scroll";
import { Link as RouterLink, useHistory } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
// Components
import Sidebar from "../Nav/Sidebar";
import Backdrop from "../Elements/Backdrop";
// project imports
import config from "../../../../config";
import { LOGOUT } from "../../../../store/actions";
// Assets - paths updated to new location
import KeyrusLogo from "../../../../assets/images/keyrus_logo.png";
import BurgerIcon from "../../../../assets/landing/svg/BurgerIcon";

export default function TopNavbar() {
  const [y, setY] = useState(window.scrollY);
  const [sidebarOpen, toggleSidebar] = useState(false);
  const history = useHistory();
  const dispatch = useDispatch();
  const { isLoggedIn, token } = useSelector((state) => state.account);

  const handleLogout = () => {
    axios
      .post(config.API_SERVER + "users/logout", { token: `${token}` }, { headers: { Authorization: `${token}` } })
      .then(() => {
        dispatch({ type: LOGOUT });
      })
      .catch(() => {
        dispatch({ type: LOGOUT });
      })
      .finally(() => {
        history.push("/");
      });
  };

  useEffect(() => {
    window.addEventListener("scroll", () => setY(window.scrollY));
    return () => {
      window.removeEventListener("scroll", () => setY(window.scrollY));
    };
  }, [y]);

  return (
    <>
      <Sidebar sidebarOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      {sidebarOpen && <Backdrop toggleSidebar={toggleSidebar} />}
      <Wrapper
        className="flexCenter animate whiteBg"
        style={
          y > 100
            ? { height: "60px", boxShadow: "0 8px 30px rgba(0, 0, 0, 0.12)" }
            : { height: "80px", boxShadow: "none" }
        }
      >
        <NavInner className="container flexSpaceCenter">
          <Link className="pointer flexNullCenter" to="home" smooth={true}>
            <img src={KeyrusLogo} alt="Keyrus" style={{ width: "120px", height: "auto" }} />
          </Link>
          <BurderWrapper className="pointer" onClick={() => toggleSidebar(!sidebarOpen)}>
            <BurgerIcon />
          </BurderWrapper>
          <UlWrapper className="flexNullCenter">
            <li className="semiBold font15 pointer">
              <Link activeClass="active" style={{ padding: "10px 15px" }} to="home" spy={true} smooth={true} offset={-80}>
                Accueil
              </Link>
            </li>
            <li className="semiBold font15 pointer">
              <Link activeClass="active" style={{ padding: "10px 15px" }} to="services" spy={true} smooth={true} offset={-80}>
                Services
              </Link>
            </li>
            <li className="semiBold font15 pointer">
              <Link activeClass="active" style={{ padding: "10px 15px" }} to="projects" spy={true} smooth={true} offset={-80}>
                Pourquoi nous
              </Link>
            </li>
            <li className="semiBold font15 pointer">
              <Link activeClass="active" style={{ padding: "10px 15px" }} to="blog" spy={true} smooth={true} offset={-80}>
                Témoignages
              </Link>
            </li>
            {/* <li className="semiBold font15 pointer">
              <Link activeClass="active" style={{ padding: "10px 15px" }} to="pricing" spy={true} smooth={true} offset={-80}>
                Tarifs
              </Link>
            </li> */}
            <li className="semiBold font15 pointer">
              <Link activeClass="active" style={{ padding: "10px 15px" }} to="contact" spy={true} smooth={true} offset={-80}>
                Contact
              </Link>
            </li>
          </UlWrapper>
          <UlWrapperRight className="flexNullCenter">
            {isLoggedIn ? (
              <>
                <li className="flexCenter">
                  <NavButtonGhost type="button" onClick={handleLogout}>
                    Déconnexion
                  </NavButtonGhost>
                </li>
                <li className="flexCenter" style={{ marginLeft: "12px" }}>
                  <NavButtonPrimary to={config.defaultPath}>Tableau de bord</NavButtonPrimary>
                </li>
              </>
            ) : (
              <li className="flexCenter">
                <NavButtonPrimary to="/login">Connexion</NavButtonPrimary>
              </li>
            )}
          </UlWrapperRight>
        </NavInner>
      </Wrapper>
    </>
  );
}

const Wrapper = styled.nav`
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 999;
`;
const NavInner = styled.div`
  position: relative;
  height: 100%;
`;
const BurderWrapper = styled.button`
  outline: none;
  border: 0px;
  background-color: transparent;
  height: 100%;
  padding: 0 15px;
  display: none;
  @media (max-width: 760px) {
    display: block;
  }
`;
const UlWrapper = styled.ul`
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;

  @media (max-width: 760px) {
    display: none;
  }
`;
const UlWrapperRight = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;

  @media (max-width: 760px) {
    display: none;
  }
`;
const NavButtonPrimary = styled(RouterLink)`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 9px 24px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
  color: #ffffff;
  background-color: #2DCFFF;
  border: 1px solid transparent;
  text-decoration: none;
  transition: all 0.2s ease;
  &:hover {
    background-color: #0FA8D6;
    color: #ffffff !important;
  }
`;
const NavButtonGhost = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 22px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
  font-family: inherit;
  color: var(--lp-text-secondary);
  background-color: transparent;
  border: 1px solid var(--lp-border);
  cursor: pointer;
  outline: none;
  transition: all 0.2s ease;
  &:hover {
    border-color: #0FA8D6;
    color: #0FA8D6;
  }
`;
