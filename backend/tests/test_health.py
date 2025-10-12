from fastapi.testclient import TestClient
import importlib.util
import sys
from pathlib import Path


def import_main_app():
    # load backend/main.py as a module regardless of PYTHONPATH
    main_path = Path(__file__).resolve().parents[1] / "main.py"
    spec = importlib.util.spec_from_file_location("backend_main", str(main_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore
    return module.app


def test_health():
    app = import_main_app()
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
