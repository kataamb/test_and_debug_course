import { useState, useEffect, useCallback } from 'react';
import { loadWasmPhysics, jsUpdateBall } from './physicsLoader';

interface Ball {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  color: string;
}

export function useWasmPhysics() {
  const [isWasmLoaded, setIsWasmLoaded] = useState(false);
  const [wasmInstance, setWasmInstance] = useState<any>(null);
  const [physicsMode, setPhysicsMode] = useState<'wasm' | 'js'>('js'); 


  useEffect(() => {
    const initWasm = async () => {
      try {
        const wasm = await loadWasmPhysics();
        setWasmInstance(wasm);
        setIsWasmLoaded(true);
        console.log('WASM loaded successfully');
      } catch (error) {
        console.warn('Using JS fallback for physics');
        setIsWasmLoaded(false);
   
      }
    };

    initWasm();
  }, []);

  // Функция обновления шарика
  const updateBall = useCallback((
    ball: Ball,
    width: number,
    height: number,
    dt: number
  ): Ball => {
    if (physicsMode === 'wasm' && wasmInstance && wasmInstance.updateBall && wasmInstance.memory) {
      // Используем WASM
      try {
        const memory = wasmInstance.memory;
        const buffer = new Float32Array(memory.buffer);
        
        // Находим свободное место в памяти - УВЕЛИЧИВАЕМ offset
        const offset = 1024; // Больше места
        
        // Записываем данные в память
        buffer[offset] = ball.x;
        buffer[offset + 1] = ball.y;
        buffer[offset + 2] = ball.vx;
        buffer[offset + 3] = ball.vy;
        
        // Вызываем WASM функцию 
        wasmInstance.updateBall(offset, width, height, ball.radius, dt); // offset, а не offset * 4
        
        // Читаем результаты
        return {
          ...ball,
          x: buffer[offset],
          y: buffer[offset + 1],
          vx: buffer[offset + 2],
          vy: buffer[offset + 3]
        };
      } catch (error) {
        console.error('WASM update failed, falling back to JS:', error);
        
        const [x, y, vx, vy] = jsUpdateBall(
          ball.x, ball.y, ball.vx, ball.vy,
          width, height, ball.radius, dt
        );
        return { ...ball, x, y, vx, vy };
      }
    } else {
      
      const [x, y, vx, vy] = jsUpdateBall(
        ball.x, ball.y, ball.vx, ball.vy,
        width, height, ball.radius, dt
      );
      return { ...ball, x, y, vx, vy };
    }
  }, [physicsMode, wasmInstance]);

  // Функция обновления всех шариков
  const updateBalls = useCallback((
    balls: Ball[],
    width: number,
    height: number,
    dt: number
  ): Ball[] => {
    return balls.map(ball => updateBall(ball, width, height, dt));
  }, [updateBall]);


  const togglePhysicsMode = useCallback(() => {
    const newMode = physicsMode === 'wasm' ? 'js' : 'wasm';
    
    if (newMode === 'wasm' && !isWasmLoaded) {
      console.warn('WASM not loaded, cannot switch to WASM mode');
      alert('WASM не загружен! Используется JavaScript.');
      return;
    }
    
    setPhysicsMode(newMode);
    console.log(`Physics mode toggled to: ${newMode}`);
  }, [physicsMode, isWasmLoaded]);

  return {
    isWasmLoaded,
    physicsMode,
    updateBall,
    updateBalls,
    togglePhysicsMode
  };
}
