from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db
from app.db.models import Project
from app.services.workspace_service import create_workspace
from app.services.docker_service import (
    create_container,
    install_requirements,
    run_project,
    get_container_url
)

router = APIRouter()

@router.post("/create")
def create_project(
    project_name: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    existing = db.query(Project).filter(Project.user_id == user.id).first()

    if existing:
        raise HTTPException(400, "User already has a project")

    path = create_workspace(user.id, project_name)

    container_id = create_container(user.id, path)

    install_requirements(container_id)
    run_project(container_id)

    url = get_container_url(container_id)

    project = Project(name=project_name, user_id=user.id)
    db.add(project)
    db.commit()

    return {
        "project": project_name,
        "url": url
    }