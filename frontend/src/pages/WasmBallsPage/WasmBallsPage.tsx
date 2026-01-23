import React from 'react';
import { WasmPhysicsCanvas } from '../../components/BallsCanvas/BallsCanvas';
import { Link } from 'react-router-dom';

export const WasmDemoPage: React.FC = () => {
  return (
    <div className="wasm-demo-page">
      <div className="wasm-demo-header">
        
        <p>Физика шариков с использованием WASM</p>
      </div>

      <div className="wasm-demo-content">
        <WasmPhysicsCanvas 
          width={800}
          height={500}
          initialBallCount={50}
        />
      </div>

      <div className="wasm-info">
        
      </div>
    </div>
  );
};
