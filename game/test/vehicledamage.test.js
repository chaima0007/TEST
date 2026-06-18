import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { VehicleDamageSystem } from '../js/vehicledamage.js';

function makeMat() {
  return {
    roughness: 0.5,
    emissive: { setHex(h) { this._hex = h; } },
    emissiveIntensity: 0,
    needsUpdate: false,
  };
}

describe('VehicleDamageSystem', () => {
  test('damage démarre à 0', () => {
    const sys = new VehicleDamageSystem();
    assert.equal(sys.getDamage(), 0);
  });

  test('addImpact() augmente les dégâts', () => {
    const sys = new VehicleDamageSystem();
    sys.addImpact(0.5);
    assert.ok(sys.getDamage() > 0, `damage attendu > 0, obtenu ${sys.getDamage()}`);
  });

  test('dégâts plafonnés à 1', () => {
    const sys = new VehicleDamageSystem();
    for (let i = 0; i < 10; i++) sys.addImpact(1.0);
    assert.equal(sys.getDamage(), 1);
  });

  test('getSpeedFactor() = 1 sous 40 % de dégâts', () => {
    const sys = new VehicleDamageSystem();
    sys.addImpact(0.3); // → 0.066, bien sous 0.40
    assert.equal(sys.getSpeedFactor(), 1.0);
  });

  test('getSpeedFactor() < 1 au-dessus de 40 % de dégâts', () => {
    const sys = new VehicleDamageSystem();
    for (let i = 0; i < 5; i++) sys.addImpact(1.0); // → damage = 1
    assert.ok(sys.getSpeedFactor() < 1.0);
  });

  test('getSpeedFactor() plancher à 0.35', () => {
    const sys = new VehicleDamageSystem();
    for (let i = 0; i < 20; i++) sys.addImpact(1.0);
    assert.ok(sys.getSpeedFactor() >= 0.35, `facteur ${sys.getSpeedFactor()} < 0.35`);
  });

  test('updateVisuals() augmente la rugosité', () => {
    const sys = new VehicleDamageSystem();
    for (let i = 0; i < 5; i++) sys.addImpact(1.0);
    const mat = makeMat();
    sys.updateVisuals(mat);
    assert.ok(mat.roughness > 0.5, `roughness ${mat.roughness} pas augmentée`);
  });

  test('updateVisuals() active emissive quand dégâts > 55 %', () => {
    const sys = new VehicleDamageSystem();
    for (let i = 0; i < 10; i++) sys.addImpact(1.0); // damage = 1
    const mat = makeMat();
    sys.updateVisuals(mat);
    assert.ok(mat.emissiveIntensity > 0, `emissiveIntensity ${mat.emissiveIntensity} attendu > 0`);
  });

  test('repair() remet les dégâts à 0 et speedFactor à 1', () => {
    const sys = new VehicleDamageSystem();
    for (let i = 0; i < 5; i++) sys.addImpact(1.0);
    const mat = makeMat();
    sys.repair(mat);
    assert.equal(sys.getDamage(), 0);
    assert.equal(sys.getSpeedFactor(), 1.0);
  });
});
