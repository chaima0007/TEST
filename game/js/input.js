const KEYMAP = {
  forward: ['KeyW', 'ArrowUp'],
  back: ['KeyS', 'ArrowDown'],
  left: ['KeyA', 'ArrowLeft'],
  right: ['KeyD', 'ArrowRight'],
  brake: ['Space'],
  nitro: ['KeyN'],
};

const TOUCH_STYLE = `
.tc-layer{position:fixed;inset:0;pointer-events:none;z-index:500;}
.tc-steer{position:absolute;left:20px;bottom:24px;display:flex;gap:14px;pointer-events:auto;}
.tc-pedals{position:absolute;right:20px;bottom:110px;display:flex;flex-direction:column;gap:14px;pointer-events:auto;}
.tc-btn{
  width:68px;height:68px;border-radius:50%;
  border:2px solid rgba(255,255,255,.45);
  background:rgba(20,24,32,.45);
  color:#fff;font-size:26px;font-weight:700;
  display:flex;align-items:center;justify-content:center;
  touch-action:none;-webkit-tap-highlight-color:transparent;
  user-select:none;transition:background .1s,border-color .1s,transform .1s;
}
.tc-btn.active{background:rgba(0,198,255,.4);border-color:#00c6ff;transform:scale(0.92);}
.tc-gas{background:rgba(81,207,102,.18);}
.tc-gas.active{background:rgba(81,207,102,.55);border-color:#51cf66;}
.tc-brake{background:rgba(255,107,107,.18);}
.tc-brake.active{background:rgba(255,107,107,.55);border-color:#ff6b6b;}
`;

function isTouchDevice() {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

export class InputManager {
  constructor() {
    this.codes = new Set();
    this.touch = { forward: false, back: false, left: false, right: false, brake: false };

    window.addEventListener('keydown', (e) => this.codes.add(e.code));
    window.addEventListener('keyup', (e) => this.codes.delete(e.code));

    if (isTouchDevice()) this._buildTouchControls();
  }

  get(action) {
    const codes = KEYMAP[action] || [];
    return codes.some((c) => this.codes.has(c)) || !!this.touch[action];
  }

  _buildTouchControls() {
    const style = document.createElement('style');
    style.textContent = TOUCH_STYLE;
    document.head.appendChild(style);

    const layer = document.createElement('div');
    layer.className = 'tc-layer';
    layer.innerHTML = `
      <div class="tc-steer">
        <button class="tc-btn" data-action="left">◀</button>
        <button class="tc-btn" data-action="right">▶</button>
      </div>
      <div class="tc-pedals">
        <button class="tc-btn tc-gas" data-action="forward">▲</button>
        <button class="tc-btn tc-brake" data-action="back">▼</button>
      </div>
    `;
    document.body.appendChild(layer);

    layer.querySelectorAll('.tc-btn').forEach((btn) => {
      const action = btn.dataset.action;
      const press = (e) => {
        e.preventDefault();
        this.touch[action] = true;
        btn.classList.add('active');
      };
      const release = (e) => {
        e.preventDefault();
        this.touch[action] = false;
        btn.classList.remove('active');
      };
      btn.addEventListener('pointerdown', press);
      btn.addEventListener('pointerup', release);
      btn.addEventListener('pointercancel', release);
      btn.addEventListener('pointerleave', release);
      btn.addEventListener('contextmenu', (e) => e.preventDefault());
    });
  }
}
