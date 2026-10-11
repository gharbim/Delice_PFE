import React from "react";
import styled from "styled-components";
import Reveal from "../Elements/Reveal";

export default function Contact() {
  return (
    <Wrapper id="contact">
      <SectionBg>
        <Glow />
        <div className="container">
          <Reveal>
            <HeaderInfo>
              <Eyebrow className="font13 semiBold">Contact</Eyebrow>
              <h1 className="font40 extraBold">Contactez-nous</h1>
              <Subtitle className="font15">Un projet, une question&nbsp;? Nos experts vous répondent rapidement.</Subtitle>
            </HeaderInfo>
          </Reveal>

          <Reveal delay={0.12}>
            <Card>
              <Form onSubmit={(e) => e.preventDefault()}>
                <FieldRow>
                  <FieldWrapper>
                    <label htmlFor="fname">
                      Prénom <Required>*</Required>
                    </label>
                    <input type="text" id="fname" name="fname" required />
                  </FieldWrapper>
                  <FieldWrapper>
                    <label htmlFor="lname">
                      Nom <Required>*</Required>
                    </label>
                    <input type="text" id="lname" name="lname" required />
                  </FieldWrapper>
                </FieldRow>

                <FieldWrapper>
                  <label htmlFor="email">
                    Email professionnel <Required>*</Required>
                  </label>
                  <input type="email" id="email" name="email" required />
                </FieldWrapper>

                <FieldWrapper>
                  <label htmlFor="phone">Téléphone</label>
                  <input type="tel" id="phone" name="phone" />
                </FieldWrapper>

                <FieldWrapper>
                  <label htmlFor="company">
                    Entreprise <Required>*</Required>
                  </label>
                  <input type="text" id="company" name="company" required />
                </FieldWrapper>

                <FieldWrapper>
                  <label htmlFor="message">
                    Message <Required>*</Required>
                  </label>
                  <textarea rows="4" id="message" name="message" required />
                </FieldWrapper>

                <ButtonInput type="submit" value="Envoyer le message" className="pointer animate" />

                <Consent>
                  En soumettant ce formulaire, vous acceptez que Delice traite les informations fournies afin de répondre à votre demande.
                </Consent>
              </Form>
            </Card>
          </Reveal>
        </div>
      </SectionBg>
    </Wrapper>
  );
}

const Wrapper = styled.section`
  width: 100%;
`;

const SectionBg = styled.div`
  position: relative;
  overflow: hidden;
  padding: 90px 0 100px 0;
  background: radial-gradient(120% 140% at 12% -10%, #1c2544 0%, #12131a 55%), #12131a;

  @media (max-width: 860px) {
    padding: 60px 0 70px 0;
  }
`;

const Glow = styled.div`
  position: absolute;
  top: -140px;
  right: -120px;
  width: 460px;
  height: 460px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(45, 207, 255, 0.28) 0%, rgba(45, 207, 255, 0) 70%);
  pointer-events: none;
`;

const HeaderInfo = styled.div`
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 560px;
  margin: 0 auto 46px auto;

  h1 {
    color: #fff;
    margin: 10px 0 12px 0;
  }
`;

const Eyebrow = styled.h4`
  display: inline-block;
  color: #2dcfff;
  letter-spacing: 0.14em;
  text-transform: uppercase;
`;

const Subtitle = styled.p`
  color: #98a2b3;
`;

const Card = styled.div`
  position: relative;
  z-index: 2;
  max-width: 640px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 24px;
  padding: 44px 44px 36px 44px;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.45);

  @media (max-width: 560px) {
    padding: 32px 24px 28px 24px;
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
`;

const FieldRow = styled.div`
  display: flex;
  gap: 16px;

  @media (max-width: 560px) {
    flex-direction: column;
    gap: 0;
  }
`;

const Required = styled.span`
  color: #e5484d;
`;

const FieldWrapper = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;

  label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #40434f;
    margin-bottom: 8px;
  }

  input,
  textarea {
    width: 100%;
    font-family: inherit;
    font-size: 0.95rem;
    color: #12131a;
    background-color: #f5f6f8;
    border: 1px solid #e7eaf0;
    border-radius: 10px;
    outline: none;
    padding: 12px 14px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
  }

  input:focus,
  textarea:focus {
    background-color: #ffffff;
    border-color: #2dcfff;
    box-shadow: 0 0 0 3px rgba(45, 207, 255, 0.15);
  }

  textarea {
    min-height: 110px;
    resize: vertical;
  }
`;

const ButtonInput = styled.input`
  border: 0;
  background-color: #2dcfff;
  width: 100%;
  padding: 15px;
  outline: none;
  color: #fff;
  font-weight: 700;
  font-size: 0.95rem;
  border-radius: 999px;
  margin-top: 6px;
  cursor: pointer;
  transition: all 0.2s ease;

  :hover {
    background-color: #0fa8d6;
  }
`;

const Consent = styled.p`
  margin: 18px 0 0 0;
  font-size: 0.78rem;
  line-height: 1.5;
  color: #8a8f9c;
  text-align: left;
`;
