"""Create a local reviewer without committing or hardcoding a password."""
import getpass
import os
import secrets
from pathlib import Path
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create local staff access for the reference-screen review (development only)."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="reviewer")
        parser.add_argument("--generate", action="store_true", help="Save a generated password to ignored .env.demo instead of prompting.")
        parser.add_argument("--password-env", help="Read the password from this environment variable.")

    def handle(self, *args, **options):
        if not settings.DEBUG or settings.ON_VERCEL:
            raise CommandError("Local demonstration accounts are disabled outside local development.")
        model = get_user_model()
        username = options["username"]
        if model.objects.filter(username=username).exists():
            self.stdout.write(f"User {username} already exists; password and permissions were not changed.")
            return
        if options["generate"]:
            credentials = Path(settings.BASE_DIR) / ".env.demo"
            if credentials.exists():
                raise CommandError(".env.demo already exists. Keep it or use --password-env; it will not be overwritten.")
            password = secrets.token_urlsafe(24)
        elif options["password_env"]:
            password = os.environ.get(options["password_env"], "")
            if not password:
                raise CommandError("The requested password environment variable is empty.")
        else:
            password = getpass.getpass("Choose a local staff password: ")
            if password != getpass.getpass("Confirm password: "):
                raise CommandError("Passwords do not match.")
        validate_password(password)
        model.objects.create_user(username=username, password=password, is_staff=True)
        if options["generate"]:
            credentials.write_text(f"RCPDL_DEMO_USERNAME={username}\nRCPDL_DEMO_PASSWORD={password}\n", encoding="utf-8")
            self.stdout.write("Generated local login saved to .env.demo (ignored by Git and deployment uploads).")
        self.stdout.write(self.style.SUCCESS(f"Local staff user {username} is ready. Open /dev/ or /staff/sign-in/."))
