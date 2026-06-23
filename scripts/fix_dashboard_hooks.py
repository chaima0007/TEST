#!/usr/bin/env python3
"""
CaelumSwarm™ — Dashboard Hooks Fixer
Supprime useCallback/useMemo de 133 dashboards (interdit par protocole).
Transforme useCallback(fn, deps) + useEffect(fn, [fn]) → useEffect(async fn, deps)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DASHBOARDS = ROOT / "app" / "dashboard"

def fix_imports(content: str) -> str:
    """Supprime useCallback et useMemo des imports React."""
    def clean_import(m):
        imports = m.group(1)
        cleaned = re.sub(r',?\s*\b(useCallback|useMemo)\b', '', imports)
        cleaned = re.sub(r'\b(useCallback|useMemo)\b,?\s*', '', cleaned)
        cleaned = re.sub(r',\s*,', ',', cleaned).strip().strip(',').strip()
        return f'import {{ {cleaned} }} from "react"'
    return re.sub(
        r'import\s*\{([^}]+)\}\s*from\s*"react"',
        clean_import,
        content
    )


def fix_usecallback_load(content: str) -> tuple[str, int]:
    """
    Transforme le pattern:
      const load = useCallback(async () => { BODY }, [D1, D2]);
      useEffect(() => { load(); }, [load]);
    En:
      useEffect(() => {
        async function load() { BODY }
        load();
      }, [D1, D2]);
    """
    fixes = 0

    # Pattern: const NAME = useCallback(async () => { ... }, [DEPS]);
    # Suivi de: useEffect(() => { NAME(); }, [NAME]);
    cb_pattern = re.compile(
        r'const\s+(\w+)\s*=\s*useCallback\s*\(\s*async\s*\(\s*\)\s*=>\s*\{(.*?)\}\s*,\s*\[([^\]]*)\]\s*\)\s*;'
        r'\s*'
        r'useEffect\s*\(\s*\(\s*\)\s*=>\s*\{\s*\1\s*\(\s*\)\s*;\s*\}\s*,\s*\[\s*\1\s*\]\s*\)\s*;',
        re.DOTALL
    )

    def replace_cb(m):
        nonlocal fixes
        name = m.group(1)
        body = m.group(2)
        deps = m.group(3).strip()
        fixes += 1
        # Indenter le body
        body_lines = body.split('\n')
        # Trouver l'indentation de base
        indented = '\n'.join('    ' + l if l.strip() else l for l in body_lines)
        return (
            f'useEffect(() => {{\n'
            f'    async function {name}() {{{indented}}}\n'
            f'    {name}();\n'
            f'  }}, [{deps}]);'
        )

    content = cb_pattern.sub(replace_cb, content)
    return content, fixes


def fix_usecallback_sync(content: str) -> tuple[str, int]:
    """
    Transforme useCallback synchrone simple:
      const fn = useCallback(() => { BODY }, [DEPS]);
    En:
      const fn = () => { BODY };
    """
    fixes = 0
    pattern = re.compile(
        r'const\s+(\w+)\s*=\s*useCallback\s*\(\s*((?:async\s*)?\(.*?\)\s*=>.*?)\s*,\s*\[[^\]]*\]\s*\)\s*;',
        re.DOTALL
    )
    def replace_sync(m):
        nonlocal fixes
        name = m.group(1)
        fn = m.group(2).strip()
        fixes += 1
        return f'const {name} = {fn};'
    content = pattern.sub(replace_sync, content)
    return content, fixes


def fix_usememo(content: str) -> tuple[str, int]:
    """
    Transforme useMemo:
      const x = useMemo(() => EXPR, [DEPS]);
    En:
      const x = EXPR;
    """
    fixes = 0
    # Pattern simple: useMemo(() => expr, [deps])
    pattern = re.compile(
        r'const\s+(\w+)\s*=\s*useMemo\s*\(\s*\(\s*\)\s*=>\s*(.*?)\s*,\s*\[[^\]]*\]\s*\)\s*;',
        re.DOTALL
    )
    def replace_memo(m):
        nonlocal fixes
        name = m.group(1)
        expr = m.group(2).strip()
        fixes += 1
        return f'const {name} = {expr};'
    content = pattern.sub(replace_memo, content)
    return content, fixes


def fix_file(path: Path) -> dict:
    original = path.read_text()
    content = original
    total_fixes = 0

    content, f1 = fix_usecallback_load(content)
    total_fixes += f1

    content, f2 = fix_usecallback_sync(content)
    total_fixes += f2

    content, f3 = fix_usememo(content)
    total_fixes += f3

    # Supprimer imports si plus aucune occurrence
    has_cb = 'useCallback' in content
    has_memo = 'useMemo' in content
    still_uses = has_cb or has_memo
    content = fix_imports(content)

    # Vérifier qu'on n'a pas cassé le fichier (contrôle simple)
    if content.count('{') != content.count('}') and abs(content.count('{') - content.count('}')) > 5:
        return {"path": str(path.relative_to(ROOT)), "status": "SKIP_BALANCE_ERROR", "fixes": 0}

    if content != original:
        path.write_text(content)

    remaining_cb = content.count('useCallback')
    remaining_memo = content.count('useMemo')

    return {
        "path": str(path.relative_to(ROOT)),
        "status": "FIXED" if total_fixes > 0 else ("CLEAN" if not still_uses else "PARTIAL"),
        "fixes": total_fixes,
        "remaining_useCallback": remaining_cb,
        "remaining_useMemo": remaining_memo,
    }


def main():
    pages = list(DASHBOARDS.rglob("page.tsx"))
    pages_with_hooks = [p for p in pages if
                        'useCallback' in p.read_text() or 'useMemo' in p.read_text()]

    print(f"CaelumSwarm™ — Dashboard Hooks Fixer")
    print(f"Pages à corriger: {len(pages_with_hooks)}/{len(pages)}")
    print("=" * 55)

    fixed = 0
    clean = 0
    partial = 0
    errors = []

    for path in sorted(pages_with_hooks):
        result = fix_file(path)
        if result["status"] == "FIXED":
            fixed += 1
        elif result["status"] == "CLEAN":
            clean += 1
        elif result["status"] == "PARTIAL":
            partial += 1
            errors.append(result)
        elif result["status"] == "SKIP_BALANCE_ERROR":
            errors.append(result)
        if result["fixes"] > 0:
            print(f"  ✓ {result['path'][-50:]} ({result['fixes']} fixes)")

    print(f"\n{'='*55}")
    print(f"  FIXES APPLIQUÉS    : {fixed}")
    print(f"  DÉJÀ PROPRES       : {clean}")
    print(f"  PARTIELS (manuels) : {partial}")
    if errors:
        print(f"\n  À CORRIGER MANUELLEMENT ({len(errors)}):")
        for e in errors[:10]:
            print(f"    - {e['path']}")
    print("=" * 55)

    # Vérification finale
    remaining = [p for p in DASHBOARDS.rglob("page.tsx")
                 if 'useCallback' in p.read_text() or 'useMemo' in p.read_text()]
    print(f"\n  Restants après fix: {len(remaining)} fichiers avec useCallback/useMemo")
    return 0 if len(remaining) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
