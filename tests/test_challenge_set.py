from scripts.build_challenge_set import build

def test_challenge_v1_balanced_and_unique():
    rows=build()
    assert len(rows)==84
    assert len({r["task_id"] for r in rows})==84
    for cls,decision in (("positive","GENERATE"),("negative","BLOCK"),("boundary","ABSTAIN")):
        xs=[r for r in rows if r["gold_class"]==cls]
        assert len(xs)==28
        assert {r["expected_decision"] for r in xs}=={decision}

def test_boundary_is_not_negative():
    assert all(r["expected_decision"]=="ABSTAIN" for r in build() if r["gold_class"]=="boundary")
