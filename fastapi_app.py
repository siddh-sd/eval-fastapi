from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from evaluation.routes import router as EvaluationRouter
from template.routes import router as TemplateRouter
from user_eval.routes import router as EvalUserRouter
from middleware.authentication.main import AuthorizationMiddleware
import sentry_sdk
from config import prod

load_dotenv()

sentry_sdk.init(
  dsn = "https://abcd.ingest.sentry.io/1234",
  debug=True,
  traces_sample_rate=1.0,
  profiles_sample_rate=1.0
)

app = FastAPI()

endpoints = [
  {
    "method": "POST",
    "regex": r"^\/userEval$",
  }
]

if prod == 'false':
  endpoints += [{
    "method": "GET",
    "regex": r"^\/docs$",
  }, {
    "method": "GET",
    "regex": r"^\/favicon.ico$",
  }, {
    "method": "GET",
    "regex": r'^\/openapi.json$',
  }
]
     
app.add_middleware(AuthorizationMiddleware, skip_endpoints=endpoints)

module_api_path = "/api/v2"
app.include_router(EvaluationRouter, prefix=module_api_path+"/evaluation")
app.include_router(EvalUserRouter, prefix=module_api_path+"/userEval")
app.include_router(TemplateRouter, prefix=module_api_path+"/template")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"], 
    allow_credentials=True
)