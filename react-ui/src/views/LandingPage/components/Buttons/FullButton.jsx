import React from "react";
import styled from "styled-components";

export default function FullButton({ title, action, border, bgColor, hoverColor, textColor, arrow }) {
  return (
    <Wrapper
      className="animate pointer radius8"
      onClick={action ? () => action() : null}
      border={border}
      bgColor={bgColor}
      hoverColor={hoverColor}
      textColor={textColor}
      arrow={arrow}
    >
      {title}
    </Wrapper>
  );
}

const Wrapper = styled.button`
  border: ${(props) =>
    props.border ? "1px solid #5B5F73" : "1px solid transparent"};
  background-color: ${(props) =>
    props.border ? "transparent" : props.bgColor ? props.bgColor : "#FC990F"};
  width: 100%;
  padding: 15px 28px;
  outline: none;
  color: ${(props) =>
    props.border ? "#5B5F73" : props.textColor ? props.textColor : "#fff"};
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: 0.01em;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: ${(props) =>
    props.border ? "none" : "0 18px 40px rgba(45, 207, 255, 0.2)"};
  transition: all 0.24s ease;
  &:hover {
    background-color: ${(props) =>
      props.border
        ? "transparent"
        : props.hoverColor
        ? props.hoverColor
        : "#C97800"};
    border-color: ${(props) => (props.bgColor ? props.bgColor : "transparent")};
  }
  &::after {
    content: ${(props) => (props.arrow ? "'→'" : "''")};
    margin-left: ${(props) => (props.arrow ? "10px" : "0")};
    font-size: 1.1rem;
    opacity: ${(props) => (props.arrow ? 1 : 0)};
    transition: margin-left 0.24s ease;
  }
`;
