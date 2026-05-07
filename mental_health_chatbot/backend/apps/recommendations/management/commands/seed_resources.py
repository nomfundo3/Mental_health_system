from django.core.management.base import BaseCommand

from apps.recommendations.models import ResourceRecommendation


RESOURCE_FIXTURES = [
    {
        "title": "Campus Counselling Booking",
        "description": "Book a session with student wellness or counselling support on campus.",
        "url": "https://www.google.com/search?q=student+counselling+services",
        "category": "general",
        "audience": "student",
        "priority": 5,
    },
    {
        "title": "Exam Stress Reset",
        "description": "A short routine for slowing down, breathing, and breaking revision into smaller steps.",
        "url": "https://www.google.com/search?q=exam+stress+coping+strategies",
        "category": "stress",
        "audience": "student",
        "priority": 4,
    },
    {
        "title": "Anxiety Grounding Exercise",
        "description": "Use the 5-4-3-2-1 sensory grounding method when your thoughts feel overwhelming.",
        "url": "https://www.google.com/search?q=5-4-3-2-1+grounding+exercise",
        "category": "anxiety",
        "audience": "all",
        "priority": 4,
    },
    {
        "title": "24/7 Crisis Support",
        "description": "Reach out to a trusted person, local emergency service, or crisis line immediately.",
        "url": "https://www.google.com/search?q=suicide+crisis+helpline+south+africa",
        "category": "crisis",
        "audience": "all",
        "priority": 10,
        "is_emergency": True,
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
