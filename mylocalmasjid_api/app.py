from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
import sentry_sdk

from mylocalmasjid_api.auth import api as auth_api
from mylocalmasjid_api.config import settings
from mylocalmasjid_api.public import api as public_api
from mylocalmasjid_api.utils.logger import logger_config

logger = logger_config(__name__)

# Initialize Sentry
sentry_sdk.init(
    dsn="https://0a4d20c2635be844f8585cd1a677fbd9@o372762.ingest.us.sentry.io/4508548172677120",
    traces_sample_rate=1.0,
    release=f"mylocalmasjid-api@{settings.VERSION}",
    environment=settings.ENV,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
    
    # Lambda-specific settings
    enable_tracing=True,
    auto_enabling_integrations=True,
    
    # Adjust sample rates based on your needs
    profiles_sample_rate=1.0,  # Performance profiling
    
    # Add Lambda context
    include_local_variables=True,
    attach_stacktrace=True,
    
    # Optional: Configure transport
    transport=sentry_sdk.transport.HttpTransport,
    shutdown_timeout=2  # Shorter timeout for Lambda
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/",
    description=settings.DESCRIPTION,
)

# Update allow_origins to restrict allowed domains
allowed_origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "https://*.salahtimez.com",
    "https://*.mylocalmasjid.com", 
    "https://*.sadikmoazzem.com",
    "https://*--salahtimez.netlify.app"  # Allow Netlify deploy previews
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://localhost:3000",
    ],
    allow_origin_regex="(http://localhost:[0-9]+|https://localhost:[0-9]+|https://.*\.(salahtimez\.com|mylocalmasjid\.com|sadikmoazzem\.com|netlify\.app))$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[],
    max_age=600
)

app.include_router(auth_api)
app.include_router(public_api)
handler = Mangum(app)
