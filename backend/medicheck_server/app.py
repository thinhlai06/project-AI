"""MediCheck AI server (FastAPI, CPU only). Run from the repo root:

    pip install -r backend/requirements.txt
    uvicorn backend.medicheck_server.app:app --host 0.0.0.0 --port 8000

Interactive API docs: http://<host>:8000/docs. Contract: backend/API.md.
Environment: MEDICHECK_MODEL_DIR (default out/onnx_final), MEDICHECK_LOOKUP (default <model dir>/lookup_name_classes.csv),
MEDICHECK_THREADS (default 4).
"""
from __future__ import annotations

import json, os
from contextlib import asynccontextmanager
from typing import List, Literal, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field, ValidationError

from .infer import Line, PillVerifier

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_DIR = os.environ.get("MEDICHECK_MODEL_DIR", os.path.join(ROOT, "out", "onnx_final"))
LOOKUP = os.environ.get("MEDICHECK_LOOKUP")  # default: lookup_name_classes.csv next to the models
STATE = {}

Session = Literal["sang", "trua", "chieu", "toi"]


class SessionLine(BaseModel):
    line_id: str = Field(..., description="Id of the prescription line in the app database (drug_line.id)")
    name: str = Field(..., description="Drug name exactly as matched by OCR (drug_line.matched_name)")
    count: int = Field(1, ge=1, le=10, description="Pills of this drug in the current dose")


class OtherLine(BaseModel):
    line_id: str
    name: str
    sessions: List[Session] = Field(default_factory=list, description="Doses where this drug is taken (for the red message)")


class VerifyRequest(BaseModel):
    session: Session = Field(..., description="Current dose: sang / trua / chieu / toi")
    session_lines: List[SessionLine] = Field(..., min_length=1, description="Drugs to take now, with pill counts (check_mode = chấm ảnh)")
    other_lines: List[OtherLine] = Field(default_factory=list, description="All other drug lines of the same prescription")
    unchecked_count: int = Field(0, ge=0, description="Pills of this dose that cannot be checked by image (reminder-only, half pills)")
    frame: Optional[List[float]] = Field(None, min_length=4, max_length=4, description="Capture frame x1,y1,x2,y2 in 0-1 image coordinates; pills whose centre is outside are ignored")


class PillOut(BaseModel):
    box: List[float] = Field(..., description="x1,y1,x2,y2 in 0-1 coordinates of the uploaded image (after EXIF rotation)")
    detector_conf: float
    status: Literal["green", "red", "yellow"]
    reason: str = Field(..., description="match | other_dose | not_in_prescription | uncertain | unmeasurable_class | extra | not_checkable")
    line_id: Optional[str] = Field(None, description="Matched line (green) or the other-dose line (red other_dose)")
    name: Optional[str] = None
    message: str = Field(..., description="Sentence to show and read aloud for this pill")


class MissingOut(BaseModel):
    line_id: str
    name: str
    count: int


class QualityOut(BaseModel):
    ok: bool
    issue: Optional[Literal["dark", "blurry"]] = None
    brightness: float
    sharpness: float


class VerifyResponse(BaseModel):
    status: Literal["green", "partial", "not_green"] = Field(..., description="green: every expected pill present and green; partial: every checkable pill green but some pills can only be checked by hand; not_green: anything else")
    summary: str = Field(..., description="One sentence to read aloud first")
    pills: List[PillOut]
    missing: List[MissingOut]
    n_expected: int
    n_detected: int
    quality: QualityOut
    timing_ms: dict
    model_version: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    STATE["verifier"] = PillVerifier(MODEL_DIR, LOOKUP, threads=int(os.environ.get("MEDICHECK_THREADS", "4")))
    yield
    STATE.clear()


app = FastAPI(title="MediCheck AI", version="1.0.0", lifespan=lifespan,
              description="Pill verification for one dose of a prescription. See backend/API.md.")


@app.get("/health")
def health():
    v = STATE.get("verifier")
    return {"ok": v is not None, "model_version": v.version if v else None}


@app.post("/v1/pills/verify", response_model=VerifyResponse)
def verify(image: UploadFile = File(..., description="Photo of the dose, JPEG, longest side 2048 px"),
           payload: str = Form(..., description="VerifyRequest as a JSON string")):
    try:
        req = VerifyRequest.model_validate_json(payload)
    except ValidationError as e:
        raise HTTPException(422, json.loads(e.json()))
    data = image.file.read()
    if not data:
        raise HTTPException(400, "empty image")
    v: PillVerifier = STATE["verifier"]
    try:
        return v.verify(data,
                        [Line(l.line_id, l.name, l.count) for l in req.session_lines],
                        [Line(l.line_id, l.name, 0, tuple(l.sessions)) for l in req.other_lines],
                        req.unchecked_count, req.session, req.frame)
    except Exception as e:  # unreadable image etc.
        raise HTTPException(400, f"cannot process image: {type(e).__name__}")


@app.post("/v1/prescriptions/parse", status_code=501)
def parse_prescription():
    """OCR of the prescription: planned for 23-29/11 (MediCheck_decisions.md sec. 7, 9)."""
    raise HTTPException(501, "not implemented yet")
