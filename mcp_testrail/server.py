import os
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

TR_URL = os.getenv("TESTRAIL_URL")
TR_USER = os.getenv("TESTRAIL_USER")
TR_KEY = os.getenv("TESTRAIL_API_KEY")

mcp = FastMCP("TestRail")

def _get_auth():
    return (TR_USER, TR_KEY)

@mcp.tool()
def get_test_cases(project_id: int, suite_id: int):
    """
    Fetches all test cases from a specific TestRail project and suite.
    """
    if not TR_URL: return "Error: TESTRAIL_URL not configured."
    url = f"{TR_URL}/index.php?/api/v2/get_cases/{project_id}&suite_id={suite_id}"
    headers = {"Content-Type": "application/json"}
    
    response = requests.get(url, headers=headers, auth=_get_auth())
    if response.status_code == 200:
        cases = response.json().get("cases", [])
        formatted = [f"ID: {c['id']} | Title: {c['title']} | Type: {c['type_id']}" for c in cases]
        return "\n".join(formatted) if formatted else "No cases found."
    return f"Failed to fetch cases: {response.status_code} - {response.text}"

@mcp.tool()
def create_test_run(project_id: int, suite_id: int, name: str):
    """
    Creates a new test run in TestRail for the given project and suite.
    """
    if not TR_URL: return "Error: TESTRAIL_URL not configured."
    url = f"{TR_URL}/index.php?/api/v2/add_run/{project_id}"
    headers = {"Content-Type": "application/json"}
    data = {
        "suite_id": suite_id,
        "name": name,
        "include_all": True
    }
    
    response = requests.post(url, headers=headers, json=data, auth=_get_auth())
    if response.status_code == 200:
        run_data = response.json()
        return f"Successfully created Test Run: {run_data['name']} (ID: {run_data['id']})"
    return f"Failed to create run: {response.status_code} - {response.text}"

@mcp.tool()
def add_test_result(run_id: int, case_id: int, status_id: int, comment: str):
    """
    Adds a result to a test case within a specific run.
    Status IDs: 1 (Passed), 2 (Blocked), 3 (Untested), 4 (Retest), 5 (Failed).
    """
    if not TR_URL: return "Error: TESTRAIL_URL not configured."
    url = f"{TR_URL}/index.php?/api/v2/add_result_for_case/{run_id}/{case_id}"
    headers = {"Content-Type": "application/json"}
    data = {
        "status_id": status_id,
        "comment": comment
    }
    
    response = requests.post(url, headers=headers, json=data, auth=_get_auth())
    if response.status_code == 200:
        return f"Result added for Case {case_id} in Run {run_id}."
    return f"Failed to add result: {response.status_code} - {response.text}"

@mcp.resource("testrail://cases/{project_id}/{suite_id}")
def testrail_cases_resource(project_id: int, suite_id: int) -> str:
    """Returns the raw JSON of all cases for a project/suite."""
    url = f"{TR_URL}/index.php?/api/v2/get_cases/{project_id}&suite_id={suite_id}"
    response = requests.get(url, auth=_get_auth())
    return response.text if response.status_code == 200 else "Error fetching resource."

if __name__ == "__main__":
    mcp.run()
