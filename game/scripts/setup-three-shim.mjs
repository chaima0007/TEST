// Le jeu importe three.js via un specifier nu ('three'), résolu dans le
// navigateur par l'importmap d'index.html, mais Node (utilisé pour les tests)
// ne connaît pas les importmaps : il faut un node_modules/three classique.
// On copie simplement la version déjà vendorée (game/vendor/three) plutôt que
// d'aller chercher sur le registre npm, pour rester cohérent avec le reste du
// projet (pas de dépendance réseau pour lancer les tests).
import { existsSync, mkdirSync, copyFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const gameRoot = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const vendorEntry = path.join(gameRoot, 'vendor', 'three', 'build', 'three.module.js');
const shimDir = path.join(gameRoot, 'node_modules', 'three');
const shimBuildDir = path.join(shimDir, 'build');
const shimEntry = path.join(shimBuildDir, 'three.module.js');
const shimPackageJson = path.join(shimDir, 'package.json');

if (!existsSync(vendorEntry)) {
  console.error(`Vendored three.js not found at ${vendorEntry}`);
  process.exit(1);
}

mkdirSync(shimBuildDir, { recursive: true });
copyFileSync(vendorEntry, shimEntry);

if (!existsSync(shimPackageJson)) {
  const fs = await import('node:fs');
  fs.writeFileSync(
    shimPackageJson,
    JSON.stringify(
      {
        name: 'three',
        version: '0.160.0',
        main: './build/three.module.js',
        module: './build/three.module.js',
        type: 'module',
      },
      null,
      2
    )
  );
}

console.log('three.js test shim ready at game/node_modules/three');
