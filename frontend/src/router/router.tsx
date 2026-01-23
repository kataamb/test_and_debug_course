/*import { createBrowserRouter } from 'react-router-dom';
import HomePage from '../pages/HomePage/HomePage';
import AdPage from '../pages/AdPage/AdPage';
import LoginPage from '../pages/LoginPage/LoginPage';


export const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/ad/:id',
    element: <AdPage />,
  },
  {
    path: '/login',
    element: <LoginPage />, // новый маршрут для логина
  },
]);
*/

// src/router/router.tsx
import { createBrowserRouter } from 'react-router-dom';
import { MainLayout } from '../layouts/MainLayout';
import { HomePage } from '../pages/HomePage/HomePage';
import { LoginPage } from '../pages/LoginPage/LoginPage';
import {AdPage} from '../pages/AdPage/AdPage';
import {WasmDemoPage} from '../pages/WasmBallsPage/WasmBallsPage';

export const router = createBrowserRouter([
  {
    // Все страницы внутри MainLayout получат Header
    element: <MainLayout />,
    children: [
      {
        path: '/',
        element: <HomePage />,
      },
      {
        path: '/login',
        element: <LoginPage />,
      },
      {
        path: '/ad/:id',
        element: <AdPage />,
      },
      {
        path: '/wasm_demo',
        element: <WasmDemoPage />,
      },

    ],
  },
]);
