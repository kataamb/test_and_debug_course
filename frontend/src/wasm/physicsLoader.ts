export interface WasmPhysics {
  updateBall: (
    ptr: number, 
    width: number, 
    height: number, 
    radius: number, 
    dt: number
  ) => void;
  memory: WebAssembly.Memory;
}

let wasmModule: WasmPhysics | null = null;

export async function loadWasmPhysics(): Promise<WasmPhysics> {
  if (wasmModule) return wasmModule;

  try {
    const response = await fetch('/physics.wasm');
    if (!response.ok) {
      throw new Error(`Failed to fetch WASM: ${response.status}`);
    }

    const buffer = await response.arrayBuffer();
    const { instance } = await WebAssembly.instantiate(buffer);
    
    wasmModule = {
      updateBall: instance.exports.updateBall as any,
      memory: instance.exports.memory as WebAssembly.Memory
    };

    console.log('WASM module loaded successfully');
    return wasmModule;
  } catch (error) {
    console.error(' Failed to load WASM:', error);
    throw error;
  }
}

// JS fallback функция
export function jsUpdateBall(
  x: number, y: number, vx: number, vy: number,
  width: number, height: number, radius: number, dt: number
): [number, number, number, number] {
  let newX = x + vx * dt;
  let newY = y + vy * dt + 0.5 * dt * dt; // гравитация
  let newVx = vx;
  let newVy = vy + 0.5 * dt;

  // Отскок от границ
  if (newX + radius > width) {
    newVx = -vx * 0.9;
    newX = width - radius;
  } else if (newX - radius < 0) {
    newVx = -vx * 0.9;
    newX = radius;
  }

  if (newY + radius > height) {
    newVy = -newVy * 0.9;
    newY = height - radius;
  } else if (newY - radius < 0) {
    newVy = -newVy * 0.9;
    newY = radius;
  }

  return [newX, newY, newVx, newVy];
}
