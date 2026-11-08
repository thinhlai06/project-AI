"""Decision-rule tests of the serving module on synthetic cosine matrices (no image needed).
Run from the repo root: python -m pytest backend/tests  (or python backend/tests/test_decide.py)"""
import os, sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from backend.medicheck_server.infer import NCLS, Line, PillVerifier  # noqa: E402

V = PillVerifier(os.path.join(ROOT, "out", "onnx_final"), threads=1)
A_NAME, B_NAME, C_NAME = "cardilopin 5mg", "hoạt huyết dưỡng não 150mg+20mg", "cosyndo b 175mg+175mg+125mcg"
CA, CB, CC = (min(V.allowed(n) & V.measurable) for n in (A_NAME, B_NAME, C_NAME))
OUTSIDE = next(c for c in sorted(V.measurable) if c not in V.allowed(A_NAME) | V.allowed(B_NAME) | V.allowed(C_NAME))


def pill(c, s=0.8, rest=0.1):
    v = np.full(NCLS, rest, np.float32); v[c] = s; return v


def test_green_dose():
    cos = np.stack([pill(CA), pill(CA), pill(CB)])
    r = V.decide(cos, [Line("a", A_NAME, 2), Line("b", B_NAME, 1)], [Line("c", C_NAME, 0, ("toi",))], session="sang")
    assert r["status"] == "green" and all(p["status"] == "green" for p in r["pills"]) and r["scene_score"] >= V.thr


def test_other_dose_is_red():
    cos = np.stack([pill(CA), pill(CC)])
    r = V.decide(cos, [Line("a", A_NAME, 2)], [Line("c", C_NAME, 0, ("toi",))], session="sang")
    st = {p["index"]: (p["status"], p["reason"]) for p in r["pills"]}
    assert r["status"] == "not_green" and st[0][0] == "green" and st[1] == ("red", "other_dose")
    assert r["scene_score"] < V.thr


def test_outside_prescription_is_red():
    cos = np.stack([pill(CA), pill(OUTSIDE, 0.9)])
    r = V.decide(cos, [Line("a", A_NAME, 2)], [], session="sang")
    assert [p["status"] for p in r["pills"]].count("red") == 1 and r["status"] == "not_green"


def test_missing_and_extra():
    r = V.decide(np.stack([pill(CA)]), [Line("a", A_NAME, 2)], [], session="sang")
    assert r["status"] == "not_green" and r["missing"] == [dict(line_id="a", name=A_NAME, count=1)]
    r = V.decide(np.stack([pill(CA), pill(CA), pill(CA, 0.3, 0.3)]), [Line("a", A_NAME, 2)], [], session="sang")
    assert r["status"] == "not_green" and r["n_detected"] == 3 and r["n_expected"] == 2


def test_uncertain_pill_is_yellow():
    cos = np.stack([pill(CA), pill(CB, 0.06, 0.06)])  # unlike every class: neither green nor red
    r = V.decide(cos, [Line("a", A_NAME, 1), Line("b", B_NAME, 1)], [], session="sang")
    assert r["status"] == "not_green" and any(p["status"] == "yellow" for p in r["pills"])


def test_reminder_only_line():
    r = V.decide(np.stack([pill(CA), pill(OUTSIDE, 0.2, 0.15)]), [Line("a", A_NAME, 1), Line("x", "thuốc không có trong danh mục", 1)], [], session="sang")
    assert r["status"] == "partial" and r["unchecked"] == 1


def test_reminder_only_pill_never_red_outside():
    # the pill of a drug the lookup does not know looks "outside the prescription": it must be yellow, not red
    r = V.decide(np.stack([pill(CA), pill(OUTSIDE, 0.9)]), [Line("a", A_NAME, 1), Line("x", "thuốc không có trong danh mục", 1)], [], session="sang")
    assert r["status"] == "partial" and [p["status"] for p in r["pills"]] == ["green", "yellow"]
    assert r["pills"][1]["reason"] == "not_checkable"


def test_unmeasurable_class_never_green():
    um = sorted(set(range(NCLS)) - V.measurable)
    name = next((n for n, cl in V.lookup.items() if cl and cl <= set(um)), None)
    if name is None:
        return
    r = V.decide(np.stack([pill(min(V.lookup[name]))]), [Line("u", name, 1)], [], session="sang")
    assert r["status"] != "green" and r["pills"][0]["status"] != "green"


if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f(); print("ok", k)
