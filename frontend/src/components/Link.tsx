import React from 'react';

interface LinkProps {
  to: string;
  children: React.ReactNode;
  onClick?: () => void;
}

export const Link: React.FC<LinkProps> = ({ to, children, onClick }) => {
  const handleClick = (e: React.MouseEvent) => {
    if (onClick) {
      e.preventDefault();
      onClick();
    }
  };

  return (
    <a href={to} onClick={handleClick}>
      {children}
    </a>
  );
};