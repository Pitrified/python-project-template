"""Application instance for uvicorn.

Entry point: uvicorn project_name.webapp.app:app
"""

from project_name.webapp.main import create_app

# Create application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn

    from project_name.params.project_name_params import get_webapp_params

    params = get_webapp_params()
    uvicorn.run(
        "project_name.webapp.app:app",
        host=params.host,
        port=params.port,
        reload=params.debug,
    )
