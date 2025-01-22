import React from "react";
import styled from "styled-components";

const AvatarWrapper = styled.div`
  display: inline-block;
  width: ${({ size }) => size || "50px"};
  height: ${({ size }) => size || "50px"};
  border-radius: 50%;
  overflow: hidden;
  border: ${({ border }) => border || "2px solid ${({ theme }) => theme.colors.primary}"};
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.1);
  }

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
`;

const Avatar = ({ src, alt, size, border }) => {
  return (
    <AvatarWrapper size={size} border={border}>
      <img src={src} alt={alt} />
    </AvatarWrapper>
  );
};

export default Avatar;
