// src/components/Login/Login.tsx
import React from 'react';
import { TextField } from '../TextField';
import { Button } from '../Button';
import { useLoginViewModel } from './Login.viewModel';

const Login: React.FC = () => {
  const { form, handleChange, handleSubmit, loading, error } = useLoginViewModel();

  return (
    <form
      onSubmit={handleSubmit}
      style={{ display: 'flex', flexDirection: 'column', gap: 10, width: 300 }}
    >
      {error && <div style={{ color: 'red' }}>{error}</div>}

      <TextField
        value={form.email}
        onChange={(value) => handleChange('email', value)}
        placeholder="Введите email"
        type="email"
      />

      <TextField
        value={form.password}
        onChange={(value) => handleChange('password', value)}
        placeholder="Введите пароль"
        type="password"
      />

      <Button type="submit" disabled={loading}>
        {'Войти'}
      </Button>
    </form>
  );
};

export default Login;
