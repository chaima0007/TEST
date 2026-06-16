const KEYMAP = {
  forward: ['KeyW', 'ArrowUp'],
  back: ['KeyS', 'ArrowDown'],
  left: ['KeyA', 'ArrowLeft'],
  right: ['KeyD', 'ArrowRight'],
  brake: ['Space'],
};

export class InputManager {
  constructor() {
    this.codes = new Set();
    window.addEventListener('keydown', (e) => this.codes.add(e.code));
    window.addEventListener('keyup', (e) => this.codes.delete(e.code));
  }

  get(action) {
    const codes = KEYMAP[action] || [];
    return codes.some((c) => this.codes.has(c));
  }
}
