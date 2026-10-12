"""
GitHub Webhook API endpoints
Handles incoming webhooks from GitHub for automatic pipeline triggers
"""
from fastapi import APIRouter, Request, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from backend.database.base import get_db
from backend.models.database_models import User, Project, Build, BuildStatus
from backend.utils.auth import get_current_active_user
from backend.services.pipeline_executor import execute_pipeline
import hmac
import hashlib
import json
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])


def verify_github_signature(payload_body: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub webhook signature"""
    if not signature:
        return False
    
    try:
        # GitHub sends signature as "sha256=<hash>"
        hash_algorithm, github_signature = signature.split('=')
        
        # Calculate expected signature
        mac = hmac.new(secret.encode(), msg=payload_body, digestmod=hashlib.sha256)
        expected_signature = mac.hexdigest()
        
        # Compare signatures
        return hmac.compare_digest(expected_signature, github_signature)
    except Exception as e:
        logger.error(f"Signature verification failed: {e}")
        return False


@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: Optional[str] = Header(None),
    x_hub_signature_256: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    GitHub webhook endpoint
    Automatically triggers builds when code is pushed to GitHub
    """
    try:
        # Get raw body for signature verification
        body = await request.body()
        
        # Parse JSON payload
        payload = await request.json()
        
        # Verify signature (optional in development, required in production)
        # webhook_secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
        # if webhook_secret and not verify_github_signature(body, x_hub_signature_256, webhook_secret):
        #     raise HTTPException(status_code=401, detail="Invalid signature")
        
        logger.info(f"Received GitHub webhook event: {x_github_event}")
        
        # Handle push events
        if x_github_event == "push":
            return await handle_push_event(payload, db)
        
        # Handle pull request events
        elif x_github_event == "pull_request":
            return await handle_pull_request_event(payload, db)
        
        # Ping event (GitHub sends this to verify webhook is working)
        elif x_github_event == "ping":
            return {
                "message": "Webhook received successfully!",
                "zen": payload.get("zen", ""),
                "hook_id": payload.get("hook_id")
            }
        
        # Other events
        else:
            return {
                "message": f"Event {x_github_event} received but not handled",
                "event": x_github_event
            }
    
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")


async def handle_push_event(payload: dict, db: Session):
    """Handle GitHub push event - trigger build"""
    try:
        # Extract information
        repository_url = payload.get("repository", {}).get("clone_url")
        branch = payload.get("ref", "").replace("refs/heads/", "")
        pusher = payload.get("pusher", {}).get("name", "GitHub User")
        commits = payload.get("commits", [])
        commit_count = len(commits)
        
        if not repository_url:
            return {"message": "No repository URL in payload"}
        
        # Find project by repository URL
        project = db.query(Project).filter(
            Project.repository_url == repository_url
        ).first()
        
        if not project:
            logger.warning(f"No project found for repository: {repository_url}")
            return {
                "message": "Project not found",
                "repository": repository_url,
                "suggestion": "Add this repository in the Projects page first"
            }
        
        # Create a new build
        build = Build(
            project_id=project.id,
            branch=branch,
            status=BuildStatus.PENDING,
            triggered_by=f"{pusher} (GitHub)",
            commit_hash=commits[0].get("id", "")[:8] if commits else None,
            commit_message=commits[0].get("message", "") if commits else None
        )
        
        db.add(build)
        db.commit()
        db.refresh(build)
        
        # Trigger pipeline execution in background
        import threading
        thread = threading.Thread(target=execute_pipeline, args=(build.id, db))
        thread.daemon = True
        thread.start()
        
        logger.info(f"Build #{build.id} triggered for project {project.name} by webhook")
        
        return {
            "message": "Build triggered successfully!",
            "build_id": build.id,
            "project": project.name,
            "branch": branch,
            "commits": commit_count,
            "pusher": pusher,
            "status": "Build started"
        }
    
    except Exception as e:
        logger.error(f"Push event handling error: {e}")
        return {"error": str(e)}


async def handle_pull_request_event(payload: dict, db: Session):
    """Handle GitHub pull request event"""
    try:
        action = payload.get("action")  # opened, closed, synchronize, etc.
        pr_number = payload.get("number")
        pr_title = payload.get("pull_request", {}).get("title")
        repository_url = payload.get("repository", {}).get("clone_url")
        
        logger.info(f"Pull request #{pr_number}: {action} - {pr_title}")
        
        # Find project
        project = db.query(Project).filter(
            Project.repository_url == repository_url
        ).first()
        
        if not project:
            return {
                "message": "Project not found",
                "repository": repository_url
            }
        
        # Trigger build for PR if action is "opened" or "synchronize"
        if action in ["opened", "synchronize"]:
            pr_branch = payload.get("pull_request", {}).get("head", {}).get("ref")
            
            build = Build(
                project_id=project.id,
                branch=pr_branch,
                status=BuildStatus.PENDING,
                triggered_by=f"PR #{pr_number} (GitHub)",
                commit_message=pr_title
            )
            
            db.add(build)
            db.commit()
            db.refresh(build)
            
            # Trigger pipeline
            import threading
            thread = threading.Thread(target=execute_pipeline, args=(build.id, db))
            thread.daemon = True
            thread.start()
            
            return {
                "message": f"Build triggered for PR #{pr_number}",
                "build_id": build.id,
                "pr_number": pr_number,
                "action": action
            }
        
        return {
            "message": f"PR {action} event received",
            "pr_number": pr_number,
            "action": action
        }
    
    except Exception as e:
        logger.error(f"PR event handling error: {e}")
        return {"error": str(e)}


@router.get("/github/setup-guide")
def get_webhook_setup_guide(current_user: User = Depends(get_current_active_user)):
    """
    Get instructions for setting up GitHub webhooks
    """
    return {
        "title": "How to Setup GitHub Webhooks",
        "steps": [
            {
                "step": 1,
                "title": "Go to Repository Settings",
                "description": "Navigate to your GitHub repository → Settings → Webhooks"
            },
            {
                "step": 2,
                "title": "Add Webhook",
                "description": "Click 'Add webhook' button"
            },
            {
                "step": 3,
                "title": "Configure Webhook",
                "description": "Set the payload URL to: https://your-domain.com/api/v1/webhooks/github"
            },
            {
                "step": 4,
                "title": "Content Type",
                "description": "Select 'application/json'"
            },
            {
                "step": 5,
                "title": "Events",
                "description": "Select 'Just the push event' or choose specific events"
            },
            {
                "step": 6,
                "title": "Activate",
                "description": "Check 'Active' and click 'Add webhook'"
            }
        ],
        "webhook_url": "https://your-domain.com/api/v1/webhooks/github",
        "supported_events": ["push", "pull_request", "ping"],
        "notes": [
            "Make sure your server is publicly accessible",
            "Add the repository to Projects first",
            "Webhook secret is optional but recommended for production",
            "Check webhook delivery logs in GitHub for debugging"
        ]
    }


@router.get("/test")
def test_webhook(current_user: User = Depends(get_current_active_user)):
    """Test webhook endpoint"""
    return {
        "status": "active",
        "message": "Webhook endpoint is working!",
        "endpoint": "/api/v1/webhooks/github",
        "supported_events": ["push", "pull_request", "ping"]
    }