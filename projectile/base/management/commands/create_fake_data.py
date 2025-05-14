from tqdm import tqdm
from faker import Faker

from django.db import transaction
from django.core.management import BaseCommand
from django.contrib.auth.hashers import make_password

from projectile.core.models import User
from projectile.server.models import Server, Category, Channel, AuditLog, Thread

fake = Faker()


class Command(BaseCommand):
    help = "fake data to make our lives easier"

    def handle(self, *args, **options):
        self.create_superuser()

        self.stdout.write("One SuperUser Created!!")
        self.stdout.write("Now Creating Fake Data.......!!")

        users = self.create_users()
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
                password="123456",
                phone="01827703876",
                is_verified=True,
            )

    def create_users(self):
        with transaction.atomic():
            emails = list(set([fake.email() for _ in range(10)]))
            try:
                users_to_create = [
                    User(
                        email=email,
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        username=fake.user_name(),
                        phone=fake.phone_number(),
                        password=make_password("123456"),
                    )
                    for email in tqdm(emails)
                ]
                User.objects.bulk_create(users_to_create, ignore_conflicts=True)
                users = User.objects.filter(email__in=emails)

                self.stdout.write("Fake Users created!")
                return users
            except Exception as e:
                self.stdout.write(str(e))

    def create_servers(self, users):
        with transaction.atomic():
            try:
                servers_to_create = [
                    Server(
                        owner=user,
                        name=f"{user.username}'s-server-{fake.word()}",
                        description=fake.paragraph(),
                    )
                    for user in tqdm(users)
                ]
                Server.objects.bulk_create(servers_to_create, ignore_conflicts=True)
                servers = Server.objects.filter(owner__in=users)
                self.stdout.write("Fake Servers created!")
                return servers
            except Exception as e:
                self.stdout.write(str(e))

    def create_categories(self, servers):
        with transaction.atomic():
            try:
                categories_to_create = [
                    Category(
                        name=f"Category: {fake.word()}",
                        server=server,
                        position=float(index),
                    )
                    for index, server in tqdm(enumerate(servers))
                ]
                Category.objects.bulk_create(
                    categories_to_create, ignore_conflicts=True
                )
                categories = Category.objects.filter(server__in=servers).select_related(
                    "server"
                )
                self.stdout.write("Fake Categories created!")
                return categories
            except Exception as e:
                self.stdout.write(str(e))

    def create_channels(self, categories):
        with transaction.atomic():
            try:
                channels_to_create = [
                    Channel(
                        name=f"Channel: {fake.word()}",
                        category=category,
                        server=category.server,
                        position=float(index),
                    )
                    for index, category in tqdm(enumerate(categories))
                ]
                Channel.objects.bulk_create(channels_to_create, ignore_conflicts=True)

                channels = Channel.objects.filter(
                    category__in=categories
                ).select_related("server", "category")

                self.stdout.write("Fake Channels created!")

                return channels

            except Exception as e:
                self.stdout.write(str(e))

    def create_threads(self, channels):
        with transaction.atomic():
            try:
                threads_to_create = [
                    Thread(
                        name=f"Thread: {fake.word()}",
                        channel=channel,
                        category=channel.category,
                        server=channel.category.server,
                    )
                    for channel in tqdm(channels)
                ]
                Thread.objects.bulk_create(threads_to_create, ignore_conflicts=True)
                self.stdout.write("Fake Threads created!")

            except Exception as e:
                self.stdout.write(str(e))
