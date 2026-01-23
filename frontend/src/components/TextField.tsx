import React from 'react';

interface TextFieldProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: 'text' | 'password' | 'email';
  disabled?: boolean;
}

export const TextField: React.FC<TextFieldProps> = ({
  value,
  onChange,
  placeholder,
  type = 'text',
  disabled = false
}) => {
  return (
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      disabled={disabled}
    />
  );
};