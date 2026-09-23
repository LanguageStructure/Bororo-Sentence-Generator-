import importlib.util
from pathlib import Path

def load_builder():
    p=Path("scripts/build_experiment_tasks.py")
    spec=importlib.util.spec_from_file_location("build_experiment_tasks",p)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_frozen_v1_task_inventory_matches_baseline():
    rows=load_builder().build()
    assert len(rows)==28
    assert [r["task_id"] for r in rows]==[f"v1-{i:03d}" for i in range(1,29)]
    assert set(r["lemma"] for r in rows)=={"nudu","meru","kodu","mako","maku"}
    assert all(r["construction"]=="indicative" for r in rows)
