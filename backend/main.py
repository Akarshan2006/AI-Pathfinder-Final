from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import sqlite3
from typing import List

from database import create_tables, get_db_connection
from schemas import (
    Candidate, Job, Company, SkillMatchRequest,
    CompanyJob, CompanyJobCreate, CompanyWithJobs, CandidateOut
)
from module_career import career_recommendation
from module_learning import generate_learning_path
from module_hiring import find_top_candidates

# Create the database and tables on startup
create_tables()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request bodies
class CareerRequest(BaseModel):
    resume_text: str
    extra_skills: list[str] = []

class LearningRequest(BaseModel):
    prompt: str

class HiringRequest(BaseModel):
    job_description: str

# Endpoints
@app.get("/")
def home():
    return {"message": "Server Running"}

# ... (Candidates and Jobs CRUD remain the same)

# Candidates CRUD
@app.get("/candidates", response_model=List[CandidateOut])
def get_candidates():
    """Retrieves all candidates from the database, ordered by last update time."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates ORDER BY is_developer DESC, updated_at DESC")
    candidates_rows = cursor.fetchall()
    candidates_out = []
    for row in candidates_rows:
        candidates_out.append(CandidateOut(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            skills=row['skills'],
            location=row['location'],
            is_developer=row['is_developer'],
            created_at=datetime.datetime.fromisoformat(row['created_at']),
            updated_at=datetime.datetime.fromisoformat(row['updated_at'])
        ))
    conn.close()
    return candidates_out

@app.post("/candidates")
def add_or_update_candidate(candidate: Candidate):
    """Adds a new candidate or updates an existing one based on email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM candidates WHERE email = ?", (candidate.email,))
        existing_candidate = cursor.fetchone()
        if existing_candidate:
            if existing_candidate['is_developer']:
                raise HTTPException(status_code=403, detail="Developer profiles cannot be modified.")
            cursor.execute(
                """
                UPDATE candidates
                SET name = ?, skills = ?, location = ?, updated_at = ?
                WHERE email = ?
                """,
                (candidate.name, candidate.skills, candidate.location, datetime.datetime.now(), candidate.email),
            )
            conn.commit()
            return {"message": "Candidate updated successfully"}
        else:
            cursor.execute(
                """
                INSERT INTO candidates (name, email, skills, location, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    candidate.name,
                    candidate.email,
                    candidate.skills,
                    candidate.location,
                    datetime.datetime.now(),
                    datetime.datetime.now(),
                ),
            )
            conn.commit()
            return {"message": "Candidate added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/candidates/{candidate_id}")
def update_candidate(candidate_id: int, candidate: Candidate):
    """Updates an existing candidate by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if the candidate is a developer
        cursor.execute("SELECT is_developer FROM candidates WHERE id = ?", (candidate_id,))
        candidate_to_update = cursor.fetchone()

        if candidate_to_update and candidate_to_update['is_developer']:
            raise HTTPException(status_code=403, detail="Developer profiles cannot be modified.")

        cursor.execute(
            """
            UPDATE candidates
            SET name = ?, email = ?, skills = ?, location = ?, updated_at = ?
            WHERE id = ?
            """,
            (candidate.name, candidate.email, candidate.skills, candidate.location, datetime.datetime.now(), candidate_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return {"message": "Candidate updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: int):
    """Deletes a candidate by ID, with a check to prevent deleting developers."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if the candidate is a developer
        cursor.execute("SELECT is_developer FROM candidates WHERE id = ?", (candidate_id,))
        candidate_to_delete = cursor.fetchone()

        if candidate_to_delete and candidate_to_delete['is_developer']:
            raise HTTPException(status_code=403, detail="Developer profiles cannot be deleted.")
        
        if not candidate_to_delete:
            raise HTTPException(status_code=404, detail="Candidate not found")

        cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
        conn.commit()

        if cursor.rowcount == 0:
            # This case should be caught by the check above, but as a fallback
            raise HTTPException(status_code=404, detail="Candidate not found")
            
        return {"message": "Candidate deleted successfully"}
    except HTTPException as http_exc:
        # Re-raise HTTP exceptions to be handled by FastAPI
        raise http_exc
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# Jobs CRUD
@app.post("/jobs", response_model=Job)
def create_job(job: Job):
    """Creates a new job."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO jobs (title, required_skills, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (job.title, job.required_skills, datetime.datetime.now(), datetime.datetime.now()),
        )
        conn.commit()
        new_job_id = cursor.lastrowid
        return {**job.dict(), "id": new_job_id}
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Job with this title already exists.")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/jobs", response_model=List[Job])
def get_jobs():
    """Retrieves all jobs from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY updated_at DESC")
    jobs = cursor.fetchall()
    conn.close()
    return [dict(row) for row in jobs]

@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: int):
    """Retrieves a single job by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(job)
    
@app.get("/jobs/title/{job_title}", response_model=Job)
def get_job_by_title(job_title: str):
    """Retrieves a single job by its title (case-insensitive)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE title = ? COLLATE NOCASE", (job_title,))
    job = cursor.fetchone()
    conn.close()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(job)

@app.put("/jobs/{job_id}")
def update_job(job_id: int, job: Job):
    """Updates an existing job."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE jobs
            SET title = ?, required_skills = ?, updated_at = ?
            WHERE id = ?
            """,
            (job.title, job.required_skills, datetime.datetime.now(), job_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"message": "Job updated successfully"}
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Job with this title already exists.")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    """Deletes a job."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"message": "Job deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# Companies CRUD (Refactored)
@app.post("/companies", response_model=Company)
def create_company(company: Company):
    """Creates a new unique company."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO companies (name, email, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (company.name, company.email, datetime.datetime.now(), datetime.datetime.now())
        )
        conn.commit()
        new_company_id = cursor.lastrowid
        return {**company.dict(), "id": new_company_id}
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=409, detail=f"Company with name '{company.name}' already exists.")
    finally:
        conn.close()

@app.get("/companies", response_model=List[CompanyWithJobs])
def get_companies():
    """Retrieves all companies with their associated job requirements."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies ORDER BY name")
    companies = cursor.fetchall()
    
    companies_with_jobs = []
    for company in companies:
        company_dict = dict(company)
        cursor.execute("SELECT * FROM company_jobs WHERE company_id = ?", (company_dict['id'],))
        jobs = cursor.fetchall()
        company_dict['jobs'] = [dict(job) for job in jobs]
        companies_with_jobs.append(company_dict)
        
    conn.close()
    return companies_with_jobs

@app.put("/companies/{company_id}", response_model=Company)
def update_company(company_id: int, company: Company):
    """Updates a company's details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE companies SET name = ?, email = ?, updated_at = ? WHERE id = ?",
            (company.name, company.email, datetime.datetime.now(), company_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Company not found")
        return {**company.dict(), "id": company_id}
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=409, detail=f"Company with name '{company.name}' already exists.")
    finally:
        conn.close()

@app.delete("/companies/{company_id}")
def delete_company(company_id: int):
    """Deletes a company and all its job associations."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE id = ?", (company_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Company not found")
    conn.close()
    return {"message": "Company deleted successfully"}

# Company-Job Association CRUD
@app.post("/companies/{company_id}/jobs", response_model=CompanyJob)
def add_job_to_company(company_id: int, job: CompanyJobCreate):
    """Adds a job requirement to a specific company."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO company_jobs (company_id, job_id, salary, required_skills, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (company_id, job.job_id, job.salary, job.required_skills, datetime.datetime.now(), datetime.datetime.now())
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {**job.dict(), "id": new_id, "company_id": company_id}

@app.put("/company_jobs/{company_job_id}", response_model=CompanyJob)
def update_company_job(company_job_id: int, job: CompanyJobCreate):
    """Updates a specific job requirement for a company."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE company_jobs SET job_id = ?, salary = ?, required_skills = ?, updated_at = ?
        WHERE id = ?
        """,
        (job.job_id, job.salary, job.required_skills, datetime.datetime.now(), company_job_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Company job link not found")
    
    cursor.execute("SELECT * FROM company_jobs WHERE id = ?", (company_job_id,))
    updated_job = cursor.fetchone()
    conn.close()
    return dict(updated_job)

@app.delete("/company_jobs/{company_job_id}")
def delete_company_job(company_job_id: int):
    """Deletes a specific job requirement from a company."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM company_jobs WHERE id = ?", (company_job_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Company job link not found")
    conn.close()
    return {"message": "Company job link deleted successfully"}


# Other endpoints from the original application

@app.post("/match_candidates")
def match_candidates(request: SkillMatchRequest):
    """Matches candidates based on a list of skills."""
    conn = get_db_connection()
    cursor = conn.cursor()
    matching_candidates = []
    try:
        # Construct a WHERE clause to check for any matching skill
        skill_conditions = [f"LOWER(skills) LIKE '%{skill.strip().lower()}%'" for skill in request.skills]
        if not skill_conditions:
            return [] # No skills provided, no candidates match

        where_clause = " OR ".join(skill_conditions)
        query = f"SELECT * FROM candidates WHERE {where_clause} ORDER BY updated_at DESC"
        
        cursor.execute(query)
        candidates = cursor.fetchall()
        matching_candidates = [dict(row) for row in candidates]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return matching_candidates

@app.post("/match_jobs")
def match_jobs(request: SkillMatchRequest):
    """Matches jobs based on a list of skills, including company information."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        request_skills_lower = {s.strip().lower() for s in request.skills}
        if not request_skills_lower:
            return []

        skill_conditions = [f"LOWER(j.required_skills) LIKE '%{s}%'" for s in request_skills_lower]
        where_clause = " OR ".join(skill_conditions)

        query = f"""
            SELECT
                j.id AS job_id,
                j.title,
                j.required_skills AS job_required_skills
            FROM jobs j
            WHERE {where_clause}
        """
        cursor.execute(query)
        jobs = cursor.fetchall()
        
        if not jobs:
            return []

        job_matches = {}
        for job in jobs:
            job_id = job['job_id']
            title_lower = job['title'].lower()
            job_skills = {s.strip().lower() for s in job['job_required_skills'].split(',') if s.strip()}
            
            if not job_skills:
                continue

            matched_skills = request_skills_lower.intersection(job_skills)
            
            # Calculate base score
            base_score = (len(matched_skills) / len(job_skills)) * 100
            
            # Calculate bonus for skills found in title
            bonus_score = 0
            for skill in matched_skills:
                if skill in title_lower:
                    bonus_score += 10
            
            # Final score, capped at 100
            score = min(base_score + bonus_score, 100)

            if score > 0:
                 job_matches[job_id] = {
                    "job_id": job_id,
                    "title": job['title'],
                    "job_required_skills": job['job_required_skills'],
                    "match_score": score,
                    "companies": []
                }

        if not job_matches:
            return []

        job_ids = list(job_matches.keys())
        company_query = f"""
            SELECT
                c.id AS company_id,
                c.name AS company_name,
                c.email AS company_email,
                cj.job_id,
                cj.salary,
                cj.required_skills
            FROM companies c
            JOIN company_jobs cj ON c.id = cj.company_id
            WHERE cj.job_id IN ({','.join('?' for _ in job_ids)})
        """
        cursor.execute(company_query, job_ids)
        company_rows = cursor.fetchall()

        for row in company_rows:
            job_id = row['job_id']
            if job_id in job_matches:
                job_matches[job_id]['companies'].append({
                    "id": row['company_id'],
                    "name": row['company_name'],
                    "email": row['company_email'],
                    "salary": row['salary'],
                    "required_skills": row['required_skills']
                })

        final_jobs = [job for job in job_matches.values() if job['companies']]
        
        sorted_jobs = sorted(final_jobs, key=lambda j: j['match_score'], reverse=True)
        return sorted_jobs

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/career")
def career_api(data: CareerRequest):
    return career_recommendation(
        resume_text=data.resume_text,
        extra_skills=data.extra_skills
    )

@app.post("/learning")
def learning_api(data: LearningRequest):
    return generate_learning_path(data.prompt)

@app.post("/hiring")
def hiring_api(data: HiringRequest):
    return find_top_candidates(data.job_description)
