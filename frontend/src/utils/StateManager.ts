// src/utils/StateManager.ts
export class StateManager<T = Record<string, any>> {
  private storageKey: string;
  private state: T;

  constructor(appName: string = 'tgApp', initialState: T = {} as T) {
    this.storageKey = `${appName}_state`;
    this.state = this.load(initialState);
  }

  private load(initialState: T): T {
    if (typeof window === 'undefined') return initialState;
    
    try {
      const saved = localStorage.getItem(this.storageKey);
      if (saved) {
        return { ...initialState, ...JSON.parse(saved) };
      }
    } catch (error) {
      console.error('Error loading state from localStorage:', error);
    }
    
    return initialState;
  }

  save(): void {
    if (typeof window === 'undefined') return;
    
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.state));
    } catch (error) {
      console.error('Error saving state to localStorage:', error);
    }
  }

  getState(): T {
    return { ...this.state };
  }

  get<K extends keyof T>(key: K): T[K] {
    return this.state[key];
  }

  set<K extends keyof T>(key: K, value: T[K]): void {
    this.state[key] = value;
    this.save();
  }

  update(updates: Partial<T>): void {
    Object.assign(this.state, updates);
    this.save();
  }

  clear(): void {
    this.state = {} as T;
    localStorage.removeItem(this.storageKey);
  }

  clearKey<K extends keyof T>(key: K): void {
    delete this.state[key];
    this.save();
  }
}

// Утилита для дебаунса
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;
  
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}
