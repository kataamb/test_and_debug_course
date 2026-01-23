import React from 'react';
import { TextField } from './TextField';

interface LabeledTextFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: 'text' | 'password' | 'email';
  error?: string;
}

export const LabeledTextField: React.FC<LabeledTextFieldProps> = ({
  label,
  value,
  onChange,
  placeholder,
  type = 'text',
  error
}) => {
  return (
    <div>
      <label>{label}</label>
      <TextField
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        type={type}
      />
      {error && <div>{error}</div>}
    </div>
  );
};