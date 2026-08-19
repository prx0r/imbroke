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
from .defai_hackathons import fetch_defai_hackathons
from .grants import fetch_grants
from .bug_bounties import fetch_bug_bounties
from .hackathon_platforms import fetch_hackathon_platforms
from .forums import fetch_forums
from .defai_protocols import fetch_defai_protocols

ALL_SOURCES = {
    # Build-to-earn
    "algora": {"fn": fetch_algora_bounties, "type": "build", "priority": "S"},
    "tether": {"fn": fetch_tether_bounties, "type": "build", "priority": "S"},
    "near": {"fn": fetch_near_funding, "type": "build", "priority": "A+"},
    "grants": {"fn": fetch_grants, "type": "build", "priority": "B"},
    "defai_hackathons": {"fn": fetch_defai_hackathons, "type": "build", "priority": "A"},
    "hackathons_space": {"fn": fetch_hackathons_space, "type": "build", "priority": "A"},
    "hackathon_platforms": {"fn": fetch_hackathon_platforms, "type": "build", "priority": "B"},
    "bug_bounties": {"fn": fetch_bug_bounties, "type": "build", "priority": "A"},
    # Serve-to-earn
    "x402": {"fn": discover_x402_services, "type": "serve", "priority": "S"},
    "apify": {"fn": discover_apify_actors, "type": "serve", "priority": "S"},
    "virtuals": {"fn": discover_virtuals_services, "type": "serve", "priority": "A+"},
    "heurist": {"fn": discover_heurist_services, "type": "serve", "priority": "A"},
    "olas": {"fn": discover_olas_mechs, "type": "serve", "priority": "A"},
    # Intelligence
    "forums": {"fn": fetch_forums, "type": "intel", "priority": "C"},
    "defai_protocols": {"fn": fetch_defai_protocols, "type": "intel", "priority": "B"},
}
