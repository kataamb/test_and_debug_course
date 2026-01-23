import React, { useRef, useEffect, useState, useCallback } from 'react';
import { loadWasmPhysics } from '../../wasm/physicsLoader';

interface Ball {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  color: string;
}

interface WasmPhysicsCanvasProps {
  width?: number;
  height?: number;
  initialBallCount?: number;
}

export const WasmPhysicsCanvas: React.FC<WasmPhysicsCanvasProps> = ({
  width = 800,
  height = 500,
  initialBallCount = 20
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>(0);
  const wasmModuleRef = useRef<any>(null);
  const ballsRef = useRef<Ball[]>([]);

  const [ballsCount, setBallsCount] = useState(0);
  const [wasmStatus, setWasmStatus] = useState<'loading' | 'loaded' | 'failed'>('loading');


  const drawFrame = useCallback((ctx: CanvasRenderingContext2D, balls: Ball[]) => {
    ctx.fillStyle = 'rgba(10, 10, 20, 0.15)';
    ctx.fillRect(0, 0, width, height);

    balls.forEach(ball => {
      ctx.beginPath();
      ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
      ctx.fillStyle = ball.color;
      ctx.shadowColor = ball.color;
      ctx.shadowBlur = 15;
      ctx.fill();
      ctx.shadowBlur = 0;
    });
  }, [width, height]);

  // ANIMATION LOOP

  const animate = useCallback(() => {
    if (!wasmModuleRef.current || !canvasRef.current) {
      animationRef.current = requestAnimationFrame(animate);
      return;
    }

    const balls = ballsRef.current;
    if (balls.length === 0) {
      animationRef.current = requestAnimationFrame(animate);
      return;
    }

    const memory = wasmModuleRef.current.memory;
    const buffer = new Float32Array(memory.buffer);

    for (let i = 0; i < balls.length; i++) {
      const ball = balls[i];
      const floatOffset = i * 4;
      const byteOffset = floatOffset * 4;

      buffer[floatOffset]     = ball.x;
      buffer[floatOffset + 1] = ball.y;
      buffer[floatOffset + 2] = ball.vx;
      buffer[floatOffset + 3] = ball.vy;

      wasmModuleRef.current.updateBall(
        byteOffset,
        width,
        height,
        ball.radius,
        1 / 60
      );

      ball.x  = buffer[floatOffset];
      ball.y  = buffer[floatOffset + 1];
      ball.vx = buffer[floatOffset + 2];
      ball.vy = buffer[floatOffset + 3];
    }

    const ctx = canvasRef.current.getContext('2d');
    if (ctx) drawFrame(ctx, balls);

    animationRef.current = requestAnimationFrame(animate);
  }, [width, height, drawFrame]);



  useEffect(() => {
    const init = async () => {
      try {
        const wasm = await loadWasmPhysics();
        wasmModuleRef.current = wasm;
        setWasmStatus('loaded');

        const initialBalls: Ball[] = [];
        for (let i = 0; i < initialBallCount; i++) {
          const r = 5 + Math.random() * 15;
          initialBalls.push({
            x: r + Math.random() * (width - r * 2),
            y: r + Math.random() * (height - r * 2),
            vx: (Math.random() - 0.5) * 8,
            vy: (Math.random() - 0.5) * 8,
            radius: r,
            color: `hsl(${Math.random() * 360}, 70%, 60%)`
          });
        }

        ballsRef.current = initialBalls;
        setBallsCount(initialBalls.length);

        animationRef.current = requestAnimationFrame(animate);
      } catch {
        setWasmStatus('failed');
      }
    };

    init();
    return () => cancelAnimationFrame(animationRef.current);
  }, [animate, width, height, initialBallCount]);



  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (wasmStatus !== 'loaded' || !canvasRef.current) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const ball: Ball = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
      vx: (Math.random() - 0.5) * 6,
      vy: (Math.random() - 0.5) * 6,
      radius: 5 + Math.random() * 20,
      color: `hsl(${Math.random() * 360}, 70%, 60%)`
    };

    ballsRef.current.push(ball);
    setBallsCount(ballsRef.current.length);
  };



  return (
    <div>
      <h2>WebAssembly Canvas Demo</h2>
      <p>WASM: {wasmStatus}</p>
      <p>Шариков: {ballsCount}</p>

      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        onClick={handleCanvasClick}
        style={{
          border: '1px solid #888',
          background: '#000',
          cursor: wasmStatus === 'loaded' ? 'pointer' : 'default'
        }}
      />

      {wasmStatus === 'loaded' && <p>Клик для добавления шарика</p>}
    </div>
  );
};

