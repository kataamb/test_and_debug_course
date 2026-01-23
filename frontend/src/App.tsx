/*
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App


*/


import React from 'react';
import './App.css';
//import ConnectionTest from './api/client/components/ConnectionTest';
import { HomePage } from './pages/HomePage/HomePage';

/*function App() {
    return ( <HomePage /> );
}
*/

//import React from 'react';
import { RouterProvider } from 'react-router-dom';
import { router } from './router/router';

const App: React.FC = () => {
  return <RouterProvider router={router} />;
};


/*function App() {
  return (
    <div className="App" style={{
      minHeight: '100vh',
      backgroundColor: '#f5f5f5',
      padding: '20px'
    }}>
      <header style={{
        textAlign: 'center',
        marginBottom: '40px',
        padding: '20px',
        backgroundColor: 'white',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}>
        <h1>Тест подключения к API</h1>
        <p>Проверяем соединение с бэкендом FastAPI</p>
      </header>

      <main style={{
        maxWidth: '800px',
        margin: '0 auto'
      }}>
        <ConnectionTest />

        <div style={{
          marginTop: '30px',
          padding: '20px',
          backgroundColor: 'white',
          borderRadius: '10px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
        }}>
          <h3>Инструкция:</h3>
          <ol style={{ textAlign: 'left', paddingLeft: '20px' }}>
            <li>Убедитесь, что бэкенд запущен на localhost:8000</li>
            <li>Нажмите "Проверить подключение"</li>
            <li>Если видите зелёный статус - всё работает!</li>
            <li>Если красный - проверьте консоль браузера (F12)</li>
          </ol>
        </div>
      </main>
    </div>
  );
}
*/

export default App;
