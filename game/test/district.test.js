import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { DistrictSystem } from '../js/district.js';

describe('DistrictSystem', () => {
  test('centre quand le joueur est à (0, 0)', () => {
    const ds = new DistrictSystem();
    assert.equal(ds.getDistrict(0, 0).id, 'centre');
  });

  test('nord quand Z < -57', () => {
    const ds = new DistrictSystem();
    assert.equal(ds.getDistrict(0, -80).id, 'nord');
  });

  test('sud quand Z > 57', () => {
    const ds = new DistrictSystem();
    assert.equal(ds.getDistrict(0, 80).id, 'sud');
  });

  test('ouest quand X < -57', () => {
    const ds = new DistrictSystem();
    assert.equal(ds.getDistrict(-80, 0).id, 'ouest');
  });

  test('est quand X > 57', () => {
    const ds = new DistrictSystem();
    assert.equal(ds.getDistrict(80, 0).id, 'est');
  });

  test('update() signale un changement au premier appel', () => {
    const ds = new DistrictSystem();
    const changed = ds.update(0, 0, null);
    assert.ok(changed !== null, 'Premier appel devrait signaler un changement');
    assert.equal(changed.id, 'centre');
  });

  test('update() retourne null si le joueur reste dans le même quartier', () => {
    const ds = new DistrictSystem();
    ds.update(0, 0, null);
    const again = ds.update(10, 10, null);
    assert.equal(again, null, 'Pas de changement attendu dans le même quartier');
  });

  test('update() signale le changement en traversant une frontière', () => {
    const ds = new DistrictSystem();
    ds.update(0, 0, null);              // centre
    const changed = ds.update(0, -80, null); // nord
    assert.ok(changed !== null);
    assert.equal(changed.id, 'nord');
  });
});
