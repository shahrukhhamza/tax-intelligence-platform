from services.entity_resolution import EntityResolver

resolver = EntityResolver()

target = "Muhammad Ahmed"

candidates = [
    "Muhammad Ahmd",
    "M Ahmed",
    "Ali Khan",
    "محمد احمد",
    "Ahmed Raza"
]

results = resolver.find_matches(
    target,
    candidates
)

print("\nMATCH RESULTS:\n")

for r in results:
    print(r)