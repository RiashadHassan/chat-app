from tqdm import tqdm
from faker import Faker

from django.db import transaction
from django.core.management import BaseCommand
from django.contrib.auth.hashers import make_password

from projectile.core.models import User
from projectile.server.models import Server, Category, Channel, Thread


class Command(BaseCommand):
    help = "Fake data to make our lives easier"

    def __init__(self):
        super().__init__()
        self.fake = Faker()
        self.default_password = "123456"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users", type=int, default=10, help="Number of users to create"
        )

    def handle(self, *args, **options):
        self.create_superuser()
        users = self.create_users(count=options["users"])
        servers = self.create_servers(users)
        categories = self.create_categories(servers)
        channels = self.create_channels(categories)
        self.create_threads(channels)

    def create_superuser(self):
        try:
            User.objects.get(email="riashad@gmail.com")
        except User.DoesNotExist:
            User.objects.create_superuser(
                username="riashad-hassan",
                first_name="Riashad",
                last_name="Hassan",
                email="riashad@gmail.com",
                password=self.default_password,
                phone="01827703876",
                is_verified=True,
            )
        self.stdout.write("One SuperUser Created!!")

    def create_users(self, count):
        with transaction.atomic():
            emails = list(set([self.fake.email() for _ in range(count)]))
            try:
                users_to_create = [
                    User(
                        email=email,
                        first_name=self.fake.first_name(),
                        last_name=self.fake.last_name(),
                        username=self.fake.user_name(),
                        phone=self.fake.phone_number(),
                        password=make_password(self.default_password),
                    )
                    for email in tqdm(emails, desc="Creating Users...")
                ]
                User.objects.bulk_create(users_to_create, ignore_conflicts=True)
                self.stdout.write("Fake Users created!")
                users = User.objects.filter(email__in=emails)
                return users
            except Exception as e:
                self.stdout.write(str(e))

    def create_servers(self, users):
        with transaction.atomic():
            servers = []
            for user in tqdm(users, desc="Creating Servers..."):
                try:
                    server = Server.objects.create(
                        owner=user,
                        name=f"{user.username}'s-server-{self.fake.word()}",
                        description=self.fake.paragraph(),
                    )
                    servers.append(server)
                except:
                    self.stdout.write(f"Error creating Server for {user.email}!")
                    continue
            self.stdout.write("Fake Servers created!")
            return servers

    def create_categories(self, servers):
        with transaction.atomic():
            categories = []
            for index, server in tqdm(
                enumerate(servers), desc="Creating Categories..."
            ):
                try:
                    category = Category.objects.create(
                        name=f"Category: {self.fake.word()}",
                        server=server,
                        position=float(index),
                    )
                    categories.append(category)
                except:
                    self.stdout.write(f"Error creating Category for {server.uid}!")
                    continue
            self.stdout.write("Fake Categories created!")
            return categories

    def create_channels(self, categories):
        with transaction.atomic():
            channels = []
            for index, category in tqdm(
                enumerate(categories), desc="Creating Channels..."
            ):
                try:
                    channel = Channel.objects.create(
                        name=f"Channel: {self.fake.word()}",
                        category=category,
                        server=category.server,
                        position=float(index),
                    )
                    channels.append(channel)
                except:
                    self.stdout.write(f"Error creating Channel for {category.uid}!")
                    continue
            self.stdout.write("Fake Channels created!")
            return channels

    def create_threads(self, channels):
        with transaction.atomic():
            threads = []
            for index, channel in tqdm(enumerate(channels), desc="Creating Threads..."):
                try:
                    thread = Thread.objects.create(
                        name=f"Thread: {self.fake.word()}",
                        channel=channel,
                        category=channel.category,
                        server=channel.category.server,
                        position=float(index),
                    )
                    threads.append(thread)
                except:
                    self.stdout.write(f"Error creating Thread for {channel.uid}!")
                    continue
            self.stdout.write("Fake Threads created!")
            return threads
