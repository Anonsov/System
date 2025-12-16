import os
import subprocess
from django.core.management.base import BaseCommand
from apps.runner.languages import LANGUAGES

class Command(BaseCommand):
    help = "Pre-pull/build cache and warm-up runner Docker images."

    def handle(self, *args, **options):
        env = os.environ.copy()
        env["DOCKER_HOST"] = env.get("DOCKER_HOST", "unix:///var/run/docker.sock")

        images = sorted({cfg["docker_image"] for cfg in LANGUAGES.values() if "docker_image" in cfg})
        if not images:
            self.stdout.write(self.style.WARNING("No docker images in LANGUAGES"))
            return

        for img in images:
            # This is cheap; if image is local it does nothing
            self.stdout.write(f"Warming {img} ...")
            subprocess.run(
                ["docker", "run", "--rm", "--network=none", img, "sh", "-lc", "true"],
                env=env,
                check=False,
            )

        self.stdout.write(self.style.SUCCESS("Warm-up complete"))