import React from "react";
import styled from "styled-components";

export default function ProjectBox({ img, title, text, action }) {
  return (
    <Wrapper>
      <ImgBtn className="aniamte pointer" onClick={action ? () => action() : null}>
        <img className="radius8" src={img} alt="project"></img>
      </ImgBtn>
      <h3 className="font20 extraBold">{title}</h3>
      <p className="font13">{text}</p>
    </Wrapper>
  );
}

const Wrapper = styled.div`
  width: 100%;
  margin-top: 30px;
  transition: transform 0.28s ease;
  img {
    width: 100%;
    height: auto;
    margin: 20px 0;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
  }
  h3 {
    padding-bottom: 10px;
  }
  &:hover {
    transform: translateY(-6px);
  }
  &:hover img {
    transform: scale(1.03);
    box-shadow: 0 24px 50px rgba(18, 19, 26, 0.18);
  }
`;
const ImgBtn = styled.button`
  background-color: transparent;
  border: 0px;
  outline: none;
  padding: 0px;
  margin: 0px;
  width: 100%;
  overflow: hidden;
  border-radius: 1rem;
`;
