import React from "react";
import styled from "styled-components";
// Assets - paths updated to new location
import QuoteIcon from "../../../../assets/landing/svg/Quotes";

function getInitials(name) {
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();
}

export default function TestimonialBox({ text, author, role }) {
  return (
    <Wrapper className="flexNullCenter flexColumn">
      <QuoteWrapper>
        <QuoteIcon fill="#2DCFFF" />
      </QuoteWrapper>
      <Text className="font14">{text}</Text>
      <Author className="flexNullCenter">
        <Avatar className="font13 extraBold">{getInitials(author)}</Avatar>
        <div>
          <AuthorName className="font14 semiBold">{author}</AuthorName>
          {role && <AuthorRole className="font12">{role}</AuthorRole>}
        </div>
      </Author>
    </Wrapper>
  );
}

const Wrapper = styled.div`
  width: 100%;
  height: 100%;
  padding: 34px 28px 28px 28px;
  margin-top: 30px;
  background-color: var(--lp-surface);
  border: 1px solid var(--lp-border);
  border-radius: 18px;
  box-shadow: 0 12px 30px rgba(18, 19, 26, 0.06);
  transition: transform 0.28s ease, box-shadow 0.28s ease;

  &:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 45px rgba(18, 19, 26, 0.12);
  }
`;
const QuoteWrapper = styled.div`
  opacity: 0.85;
  margin-bottom: 6px;

  svg {
    width: 30px;
    height: auto;
  }
`;
const Text = styled.p`
  color: var(--lp-text);
  line-height: 1.6;
  padding-bottom: 26px;
`;
const Author = styled.div`
  margin-top: auto;
`;
const Avatar = styled.div`
  width: 38px;
  height: 38px;
  min-width: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  color: #ffffff;
  background: linear-gradient(135deg, #2dcfff 0%, #0fa8d6 100%);
`;
const AuthorName = styled.p`
  color: var(--lp-text);
`;
const AuthorRole = styled.p`
  color: var(--lp-text-secondary);
  margin-top: 2px;
`;
