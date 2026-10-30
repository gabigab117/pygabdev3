"""Les captures d'une validation (skill `captures`) : chaque page de pygabdev3, au
téléphone et à l'ordinateur, avec le compte de démonstration connecté si besoin.

Une capture se nomme, puis donne son chemin : `01-accueil=/`. Un bouton à ouvrir
avant la capture suit un « @ », par son nom accessible : `02-menu=/@Menu`.
Plusieurs « @ » se suivent, dans l'ordre, et un « ~ » attend autant de
millisecondes, le temps d'une animation : `02-menu=/@Menu~800`.
"""

import argparse
import re
from pathlib import Path

from playwright.sync_api import Page, sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

SITE = "http://localhost:8000"

# The phone of a visitor, the computer of a prospect.
DEVICES = {
    "telephone": {
        "viewport": {"width": 390, "height": 844},
        "device_scale_factor": 2,
        "is_mobile": True,
        "has_touch": True,
    },
    "ordinateur": {
        "viewport": {"width": 1440, "height": 900},
        "device_scale_factor": 1,
    },
}

# Shown to a signed-in account on the public pages, never to a visitor.
WAGTAIL_USERBAR = "wagtail-userbar"

# This file lives in .claude/skills/captures/, in the repository.
REPOSITORY = Path(__file__).resolve().parents[3]


def demo_password() -> str:
    """The password of the demo account, as .env.example gives it."""
    text = (REPOSITORY / ".env.example").read_text()
    match = re.search(r"^DEMO_PASSWORD=(.+)$", text, re.MULTILINE)
    if not match:
        raise SystemExit("DEMO_PASSWORD manque dans .env.example.")
    return match.group(1).strip()


def decline_cookies(page: Page) -> None:
    """Decline the cookie bar once, so that it covers no capture."""
    page.goto(f"{SITE}/")
    try:
        page.locator(".cookie-consent__decline").click(timeout=5000)
    except PlaywrightTimeoutError:
        return  # No cookie group to consent to, hence no bar.
    page.wait_for_load_state("networkidle")


def sign_in(page: Page, password: str) -> None:
    """Sign in on the login page of the Django admin, where the back office sends a
    visitor: its address comes from the .env, so it is followed, never written here."""
    page.goto(f"{SITE}/customers/dashboard/")
    page.locator("#id_username").fill("demo")
    page.locator("#id_password").fill(password)
    page.locator("#login-form [type=submit]").click()
    page.wait_for_url("**/customers/dashboard/")


# The steps after the path of a page: « @ » opens a button, by its exact
# accessible name; « ~ » waits that many milliseconds.
STEP = re.compile(r"([@~])([^@~]+)")


def shoot(page: Page, target: str, file: Path) -> None:
    path = re.split("[@~]", target, maxsplit=1)[0]
    page.goto(f"{SITE}{path}")
    page.wait_for_load_state("networkidle")
    page.add_style_tag(content=f"{WAGTAIL_USERBAR} {{ display: none !important; }}")
    for step, value in STEP.findall(target[len(path) :]):
        if step == "~":
            page.wait_for_timeout(int(value))
            continue
        page.get_by_role("button", name=value, exact=True).first.click()
        # The menu or the modal opens with an animation.
        page.wait_for_timeout(500)
    page.evaluate("document.fonts.ready")
    page.screenshot(path=file, full_page=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Le dossier des captures, dans le scratchpad.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Connecter le compte de démonstration avant les captures.",
    )
    parser.add_argument(
        "--device",
        choices=DEVICES,
        help="Un seul gabarit, pour un bouton qui n'existe qu'à cette taille.",
    )
    parser.add_argument(
        "shots", nargs="+", metavar="nom=/chemin", help="Une capture par page."
    )
    args = parser.parse_args()
    shots = [shot.split("=", 1) for shot in args.shots]
    password = demo_password() if args.demo else ""
    devices = [args.device] if args.device else list(DEVICES)
    args.out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for device in devices:
            context = browser.new_context(
                **DEVICES[device],
                locale="fr-FR",
                timezone_id="Europe/Paris",
                color_scheme="light",
            )
            page = context.new_page()
            decline_cookies(page)
            if args.demo:
                sign_in(page, password)
            for name, target in shots:
                file = args.out / f"{name}-{device}.png"
                shoot(page, target, file)
                print(file)
            context.close()
        browser.close()


if __name__ == "__main__":
    main()
