import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { SignalAgent } from '../js/signal.js';

const ROAD_XS = [-95, -57, -19, 19, 57, 95];
const ROAD_ZS = [-95, -57, -19, 19, 57, 95];
function makeScene() { return { add: () => {} }; }

// Signal [0] = i=1,j=1 → offset = (1*5+1*3)%20 = 8
// État à t+offset : green si < 10, yellow si < 12, sinon red
// t=0 → (0+8)%20=8 → green
// t=5 → (5+8)%20=13 → red
// t=12 → (12+8)%20=0 → green

describe('SignalAgent', () => {
  test('crée 16 feux pour les croisements intérieurs (4×4)', () => {
    const sa = new SignalAgent(makeScene(), ROAD_XS, ROAD_ZS);
    assert.equal(sa.getSignalCount(), 16);
  });

  test('premier feu en vert au démarrage (t=0, offset=8 → phase=8)', () => {
    const sa = new SignalAgent(makeScene(), ROAD_XS, ROAD_ZS);
    assert.equal(sa.getSignals()[0].state, 'green');
  });

  test('passe au rouge à t=5 (phase=13)', () => {
    const sa = new SignalAgent(makeScene(), ROAD_XS, ROAD_ZS);
    sa.update(5);
    assert.equal(sa.getSignals()[0].state, 'red');
  });

  test('repasse au vert à t=12 (cycle complet, phase=0)', () => {
    const sa = new SignalAgent(makeScene(), ROAD_XS, ROAD_ZS);
    sa.update(12);
    assert.equal(sa.getSignals()[0].state, 'green');
  });

  test('isViolation() retourne true quand rouge et vitesse > 15 km/h', () => {
    const sa = new SignalAgent(makeScene(), ROAD_XS, ROAD_ZS);
    sa.update(5); // signal[0] est rouge
    const sig = sa.getSignals()[0];
    assert.ok(sa.isViolation(sig.x, sig.z, 50), 'Infraction non détectée');
  });

  test('isViolation() retourne false quand vitesse < 15 km/h (arrêt au rouge)', () => {
    const sa = new SignalAgent(makeScene(), ROAD_XS, ROAD_ZS);
    sa.update(5);
    const sig = sa.getSignals()[0];
    assert.ok(!sa.isViolation(sig.x, sig.z, 10));
  });
});
