import React from "react";
import styled from "styled-components";
// Assets - paths updated to new location
import RollerIcon from "../../../../assets/landing/svg/Services/RollerIcon";
import MonitorIcon from "../../../../assets/landing/svg/Services/MonitorIcon";
import BrowserIcon from "../../../../assets/landing/svg/Services/BrowserIcon";
import PrinterIcon from "../../../../assets/landing/svg/Services/PrinterIcon";

export default function ServiceBox({ icon, title, subtitle }) {
  let getIcon;

  switch (icon) {
    case "roller":
      getIcon = <RollerIcon />;
      break;
    case "monitor":
      getIcon = <MonitorIcon />;
      break;
    case "browser":
      getIcon = <BrowserIcon />;
      break;
    case "printer":
      getIcon = <PrinterIcon />;
      break;
    default:
      getIcon = <RollerIcon />;
      break;
  }

  return (
    <Wrapper className="flex flexColumn">
      <IconStyle>{getIcon}</IconStyle>
      <TitleStyle className="font20 extraBold">{title}</TitleStyle>
      <SubtitleStyle className="font13">{subtitle}</SubtitleStyle>
    </Wrapper>
  );
}

const Wrapper = styled.div`
  width: 100%;
  padding: 28px 20px;
  border-radius: 18px;
  transition: transform 0.28s ease, box-shadow 0.28s ease, background-color 0.28s ease;

  &:hover {
    transform: translateY(-6px);
    background-color: var(--lp-bg-alt);
    box-shadow: 0 20px 45px rgba(18, 19, 26, 0.08);
  }
`;
const IconStyle = styled.div`
  @media (max-width: 860px) {
    margin: 0 auto;
  }
`;
const TitleStyle = styled.h2`
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
  padding: 40px 0;
  @media (max-width: 860px) {
    padding: 20px 0;
  }
`;
const SubtitleStyle = styled.p`
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
`;
