from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database.database import initialize_database
from app.database.database import initialize_database
from app.job_service import (
    add_job,
    get_all_jobs,
    get_job_by_id,
    update_job,
    delete_job,
    search_jobs,
    update_job_status,
    update_job_stage,
)
from app.ai.analyzer import analyze_job_description


# Create FastAPI application
app = FastAPI(
    title="JobHunt AI",
    description="AI-powered job tracking and job description analysis system.",
    version="1.0.0",
)


# Initialize database when application starts
@app.on_event("startup")
def startup_event():
    initialize_database()


# -----------------------------
# Request Models
# -----------------------------

class JobCreate(BaseModel):
    company: str
    role: str = ""
    contact_name: str = ""
    contact_role: str = ""
    source: str = ""
    stage: str = "Saved"
    status: str = "Active"
    priority: str = "Medium"
    deadline: str = ""
    next_action: str = ""
    notes: str = ""


class JobUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    contact_name: str | None = None
    contact_role: str | None = None
    source: str | None = None
    stage: str | None = None
    status: str | None = None
    priority: str | None = None
    deadline: str | None = None
    next_action: str | None = None
    notes: str | None = None


class JobAnalysisRequest(BaseModel):
    job_description: str


class StatusUpdate(BaseModel):
    status: str


class StageUpdate(BaseModel):
    stage: str


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def root():
    return {
        "application": "JobHunt AI",
        "status": "running",
        "message": "Welcome to JobHunt AI",
    }


# -----------------------------
# Job Endpoints
# -----------------------------

@app.post("/jobs")
def create_job(job: JobCreate):

    job_id = add_job(
        company=job.company,
        role=job.role,
        contact_name=job.contact_name,
        contact_role=job.contact_role,
        source=job.source,
        stage=job.stage,
        status=job.status,
        priority=job.priority,
        deadline=job.deadline,
        next_action=job.next_action,
        notes=job.notes,
    )

    return {
        "message": "Job opportunity created successfully",
        "job_id": job_id,
    }


@app.get("/jobs")
def get_jobs():

    return get_all_jobs()


@app.get("/jobs/{job_id}")
def get_job(job_id: int):

    job = get_job_by_id(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job opportunity not found",
        )

    return job


@app.put("/jobs/{job_id}")
def edit_job(job_id: int, job: JobUpdate):

    updated = update_job(
        job_id=job_id,
        company=job.company,
        role=job.role,
        contact_name=job.contact_name,
        contact_role=job.contact_role,
        source=job.source,
        stage=job.stage,
        status=job.status,
        priority=job.priority,
        deadline=job.deadline,
        next_action=job.next_action,
        notes=job.notes,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Job opportunity not found or nothing to update",
        )

    return {
        "message": "Job opportunity updated successfully"
    }


@app.delete("/jobs/{job_id}")
def remove_job(job_id: int):

    deleted = delete_job(job_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Job opportunity not found",
        )

    return {
        "message": "Job opportunity deleted successfully"
    }


# -----------------------------
# Search
# -----------------------------

@app.get("/jobs/search/{keyword}")
def search_job_opportunities(keyword: str):

    return search_jobs(keyword)


# -----------------------------
# Status / Stage
# -----------------------------

@app.patch("/jobs/{job_id}/status")
def change_status(
    job_id: int,
    data: StatusUpdate,
):

    updated = update_job_status(
        job_id,
        data.status,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Job opportunity not found",
        )

    return {
        "message": "Status updated successfully"
    }


@app.patch("/jobs/{job_id}/stage")
def change_stage(
    job_id: int,
    data: StageUpdate,
):

    updated = update_job_stage(
        job_id,
        data.stage,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Job opportunity not found",
        )

    return {
        "message": "Stage updated successfully"
    }


# -----------------------------
# AI Job Analyzer
# -----------------------------

@app.post("/analyze-job")
def analyze_job(request: JobAnalysisRequest):

    try:

        analysis = analyze_job_description(
            request.job_description
        )

        return {
            "message": "Job description analyzed successfully",
            "analysis": analysis,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(error)}",
        )