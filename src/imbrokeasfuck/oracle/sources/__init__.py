"""Source registry — all opportunity sources."""
from .algora import fetch_algora_bounties
from .x402 import discover_x402_services
from .tether import fetch_tether_bounties
from .near import fetch_near_funding
from .apify import discover_apify_actors
from .virtuals import discover_virtuals_services
from .heurist import discover_heurist_services
from .olas import discover_olas_mechs
from .hackathons_space import fetch_hackathons_space

ALL_SOURCES = {
    "algora": {"fn": fetch_algora_bounties, "type": "build_to_earn", "priority": "S"},
    "x402": {"fn": discover_x402_services, "type": "serve_to_earn", "priority": "S"},
    "tether": {"fn": fetch_tether_bounties, "type": "build_to_earn", "priority": "S"},
    "near": {"fn": fetch_near_funding, "type": "build_to_earn", "priority": "A+"},
    "apify": {"fn": discover_apify_actors, "type": "serve_to_earn", "priority": "S"},
    "virtuals": {"fn": discover_virtuals_services, "type": "serve_to_earn", "priority": "A+"},
    "heurist": {"fn": discover_heurist_services, "type": "serve_to_earn", "priority": "A"},
    "olas": {"fn": discover_olas_mechs, "type": "serve_to_earn", "priority": "A"},
    "hackathons_space": {"fn": fetch_hackathons_space, "type": "build_to_earn", "priority": "A"},
}
