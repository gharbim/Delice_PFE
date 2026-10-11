
import React from "react";
import styled from "styled-components";
import { Link } from "react-scroll";
import { Link as RouterLink, useHistory } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";

// Project imports
import config from "../../../../config";
import { LOGOUT } from "../../../../store/actions";

// Assets
import CloseIcon from "../../../../assets/landing/svg/CloseIcon";
import LogoIcon from "../../../../assets/landing/svg/Logo";

export default function Sidebar({ sidebarOpen, toggleSidebar }) {
  const history = useHistory();
  const dispatch = useDispatch();
  const { isLoggedIn, token } = useSelector((state) => state.account);

  const handleLogout = () => {
    toggleSidebar(!sidebarOpen);

    axios
      .post(
        config.API_SERVER + "users/logout",
        { token: `${token}` },
        { headers: { Authorization: `${token}` } }
      )
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

  return (
    <Wrapper className="animate" sidebarOpen={sidebarOpen}>
      <SidebarHeader className="flexSpaceCenter">
        <div className="flexNullCenter">
          <LogoIcon />
          <h1
            className="whiteColor font20"
            style={{ marginLeft: "15px" }}
          >
            Keyrus
          </h1>
        </div>

        <CloseBtn
          onClick={() => toggleSidebar(!sidebarOpen)}
          className="animate pointer"
          aria-label="Fermer le menu"
        >
          <CloseIcon />
        </CloseBtn>
      </SidebarHeader>

      <UlStyle className="flexNullCenter flexColumn">
        <li className="semiBold font15 pointer">
          <Link
            onClick={() => toggleSidebar(!sidebarOpen)}
            activeClass="active"
            className="whiteColor"
            style={{ padding: "10px 15px" }}
            to="home"
            spy={true}
            smooth={true}
            offset={-60}
          >
            Accueil
          </Link>
        </li>

        <li className="semiBold font15 pointer">
          <Link
            onClick={() => toggleSidebar(!sidebarOpen)}
            activeClass="active"
            className="whiteColor"
            style={{ padding: "10px 15px" }}
            to="services"
            spy={true}
            smooth={true}
            offset={-60}
          >
            Services
          </Link>
        </li>

        <li className="semiBold font15 pointer">
          <Link
            onClick={() => toggleSidebar(!sidebarOpen)}
            activeClass="active"
            className="whiteColor"
            style={{ padding: "10px 15px" }}
            to="projects"
            spy={true}
            smooth={true}
            offset={-60}
          >
            Pourquoi nous
          </Link>
        </li>

        <li className="semiBold font15 pointer">
          <Link
            onClick={() => toggleSidebar(!sidebarOpen)}
            activeClass="active"
            className="whiteColor"
            style={{ padding: "10px 15px" }}
            to="blog"
            spy={true}
            smooth={true}
            offset={-60}
          >
            Témoignages
          </Link>
        </li>

        <li className="semiBold font15 pointer">
          <Link
            onClick={() => toggleSidebar(!sidebarOpen)}
            activeClass="active"
            className="whiteColor"
            style={{ padding: "10px 15px" }}
            to="pricing"
            spy={true}
            smooth={true}
            offset={-60}
          >
            Tarifs
          </Link>
        </li>

        <li className="semiBold font15 pointer">
          <Link
            onClick={() => toggleSidebar(!sidebarOpen)}
            activeClass="active"
            className="whiteColor"
            style={{ padding: "10px 15px" }}
            to="contact"
            spy={true}
            smooth={true}
            offset={-60}
          >
            Contact
          </Link>
        </li>
      </UlStyle>

      <UlStyle className="flexSpaceCenter">
        {isLoggedIn ? (
          <>
            <li>
              <SidebarButtonGhost
                type="button"
                onClick={handleLogout}
              >
                Déconnexion
              </SidebarButtonGhost>
            </li>

            <li style={{ marginLeft: "12px" }}>
              <SidebarButtonPrimary
                to={config.defaultPath}
                onClick={() => toggleSidebar(!sidebarOpen)}
              >
                Tableau de bord
              </SidebarButtonPrimary>
            </li>
          </>
        ) : (
          <>
            <li>
              <SidebarButtonGhost
                as={RouterLink}
                to="/login"
                onClick={() => toggleSidebar(!sidebarOpen)}
              >
                Connexion
              </SidebarButtonGhost>
            </li>

            <li style={{ marginLeft: "12px" }}>
              <SidebarButtonPrimary
                to="/login"
                onClick={() => toggleSidebar(!sidebarOpen)}
              >
                Commencer
              </SidebarButtonPrimary>
            </li>
          </>
        )}
      </UlStyle>
    </Wrapper>
  );
}

const Wrapper = styled.nav`
  width: 400px;
  height: 100vh;
  position: fixed;
  top: 0;
  padding: 0 30px;
  right: ${(props) => (props.sidebarOpen ? "0px" : "-400px")};
  z-index: 9999;
  background-color: #1b1b1b;

  @media (max-width: 400px) {
    width: 100%;
  }
`;

const SidebarHeader = styled.div`
  padding: 20px 0;
`;

const CloseBtn = styled.button`
  border: 0;
  outline: none;
  background-color: transparent;
  padding: 10px;
  cursor: pointer;
`;

const UlStyle = styled.ul`
  padding: 40px;

  li {
    margin: 20px 0;
  }
`;

const SidebarButtonPrimary = styled(RouterLink)`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 9px 22px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
  color: #ffffff;
  background-color: #2dcfff;
  border: 1px solid transparent;
  text-decoration: none;
  transition: all 0.2s ease;

  &:hover {
    background-color: #0fa8d6;
    color: #ffffff !important;
  }
`;

const SidebarButtonGhost = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 20px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
  font-family: inherit;
  color: #ffffff;
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.4);
  text-decoration: none;
  cursor: pointer;
  outline: none;
  transition: all 0.2s ease;

  &:hover {
    border-color: #2dcfff;
    color: #2dcfff;
  }
`;