from django.core.management.base import BaseCommand

from apps.recommendations.models import ResourceRecommendation


RESOURCE_FIXTURES = [
    {
        "title": "SADAG Higher Learning Support",
        "description": "A South Africa-focused higher-learning support entry point for student and staff mental health outreach, talks, and campus support connections.",
        "url": "https://www.sadag.org/index.php?Itemid=510&catid=11&id=3025%3Ahigher-learning-contact-page&option=com_content&view=article",
        "category": "general",
        "audience": "student",
        "priority": 5,
        "tags": ["south-africa", "student", "campus", "counselling"],
    },
    {
        "title": "SADAG Mental Health Helpline",
        "description": "South African mental health support for anxiety, stress, and emotional overwhelm. Helpline: 0800 21 22 23. Office line: 011 234 4837.",
        "url": "https://www.sadag.org/",
        "category": "stress",
        "audience": "all",
        "priority": 8,
        "tags": ["south-africa", "stress", "helpline", "sadag"],
    },
    {
        "title": "SADAG Suicide Crisis Support",
        "description": "For urgent emotional crisis support in South Africa, SADAG lists a 24-hour Suicide Crisis Helpline: 0800 567 567.",
        "url": "https://www.sadag.org/suicide-crisis",
        "category": "crisis",
        "audience": "all",
        "priority": 10,
        "is_emergency": True,
        "tags": ["south-africa", "crisis", "suicide", "emergency", "sadag"],
    },
    {
        "title": "LifeLine South Africa Counselling",
        "description": "National counselling support for trauma, suicide, relationship problems, and emotional distress. Counselling line: 0861 322 322.",
        "url": "https://lifelinesa.co.za/",
        "category": "general",
        "audience": "all",
        "priority": 7,
        "tags": ["south-africa", "counselling", "lifeline", "general"],
    },
    {
        "title": "National Department of Health Mental Health",
        "description": "Official South African mental health information and policy resources. National helpline listed there: 0800 012 322.",
        "url": "https://www.health.gov.za/mental-health/",
        "category": "general",
        "audience": "all",
        "priority": 6,
        "tags": ["south-africa", "government", "mental-health", "official"],
    },
    {
        "title": "South African Federation for Mental Health",
        "description": "A long-standing South African mental health organisation with advocacy, information resources, and links to support services across provinces.",
        "url": "https://www.safmh.org/",
        "category": "anxiety",
        "audience": "all",
        "priority": 6,
        "tags": ["south-africa", "anxiety", "education", "advocacy"],
    },
]


class Command(BaseCommand):
    help = "Seed starter support resources for the mental health chatbot demo."

    def handle(self, *args, **options):
        for item in RESOURCE_FIXTURES:
            ResourceRecommendation.objects.update_or_create(
                title=item["title"],
                defaults=item,
            )
        self.stdout.write(self.style.SUCCESS("Support resources seeded successfully."))
