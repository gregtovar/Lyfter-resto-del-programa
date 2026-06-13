"""
Solar System — Multiple Inheritance Demo
========================================

Inheritance tree created by Greg 
-----------------------------------

        CelestialBody   Luminous   GravitationalBody   OrbitalBody   GalacticStructure
               │            │              │                 │                │
               └────────────┴──────────────┘                │                │
                            │                               │                │
                          Star ──────────────────────────── ┘                │
                            │                                                 │
                           Sun                                                │
                                                                              │
        CelestialBody   GravitationalBody   OrbitalBody                      │
               └────────────┴──────────────┘                                 │
                            │                                                 │
                          Planet                                               │
                         /      \                                              │
                      Earth    Mars (etc.)                                     │
                                                                               │
        CelestialBody   GalacticStructure   GravitationalBody                 │
               └────────────┴──────────────────┘                              │
                            │                                                  │
                          Galaxy                                               │
                            │                                                  │
                         MilkyWay ─────────────────────────────────────────── ┘
"""


# ══════════════════════════════════════════════════════════
#  1.  BASE / MIXIN CLASSES
#      Each captures one clear responsibility.
# ══════════════════════════════════════════════════════════

class CelestialBody:
    # Root mixin: any named object in space with a physical size.

    def __init__(self, name: str, diameter_km: float, **kwargs):
        super().__init__(**kwargs)          # cooperative super() for MRO chain
        self.name = name
        self.diameter_km = diameter_km

    def describe(self) -> str:
        return (f"[CelestialBody] {self.name} — "
                f"diameter: {self.diameter_km:,.0f} km")


class Luminous:
    # Mixin: objects that emit their own light."""

    def __init__(self, luminosity_suns: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.luminosity_suns = luminosity_suns

    def emit_light(self) -> str:
        return (f"[Luminous] {self.name} emits light at "
                f"{self.luminosity_suns:,.2f}× solar luminosity.")


# Mixin: objects with significant gravitational influence.
class GravitationalBody:

    def __init__(self, mass_kg: float, **kwargs):
        super().__init__(**kwargs)
        self.mass_kg = mass_kg

    def gravitational_pull(self) -> str:
        G = 6.674e-11
        radius_m = getattr(self, "diameter_km", 1) * 1000 / 2
        surface_g = (G * self.mass_kg) / (radius_m ** 2) if radius_m else 0
        return (f"[Gravity] {self.name} — mass: {self.mass_kg:.3e} kg, "
                f"surface gravity ≈ {surface_g:.2f} m/s²")


# 
# 
# Mixin: objects that orbit a parent body."""
#
class OrbitalBody:

    def __init__(self, orbital_period_days: float,
                 orbital_radius_km: float, **kwargs):
        super().__init__(**kwargs)
        self.orbital_period_days = orbital_period_days
        self.orbital_radius_km = orbital_radius_km

    def orbit_info(self) -> str:
        years = self.orbital_period_days / 365.25
        return (f"[Orbit] {self.name} orbits every "
                f"{self.orbital_period_days:,.1f} days ({years:.2f} years) "
                f"at {self.orbital_radius_km:,.0f} km from its parent.")


class GalacticStructure:
    # Mixin: large-scale structures that contain star systems.

    def __init__(self, num_stars: float, diameter_light_years: float, **kwargs):
        super().__init__(**kwargs)
        self.num_stars = num_stars
        self.diameter_light_years = diameter_light_years

    def galactic_info(self) -> str:
        return (f"[Galaxy] {self.name} spans "
                f"{self.diameter_light_years:,.0f} light-years "
                f"and contains ~{self.num_stars:.2e} stars.")


# ══════════════════════════════════════════════════════════
#  2.  COMPOSITE CLASSES  (multiple inheritance begins here)
# ══════════════════════════════════════════════════════════

class Star(CelestialBody, Luminous, GravitationalBody):
    """
    A star: a celestial body that glows and exerts gravity.
    Inherits from → CelestialBody, Luminous, GravitationalBody
    """

    def __init__(self, star_type: str = "G-type", **kwargs):
        super().__init__(**kwargs)
        self.star_type = star_type

    def summary(self) -> str:
        lines = [
            f"\n  ⭐  Star: {self.name}  ({self.star_type})",
            f"     {self.describe()}",
            f"     {self.emit_light()}",
            f"     {self.gravitational_pull()}",
        ]
        return "\n".join(lines)


"""
A planet: a body with gravity that orbits a star.
Inherits from → CelestialBody, GravitationalBody, OrbitalBody
"""



class Planet(CelestialBody, GravitationalBody, OrbitalBody):


    def __init__(self, has_atmosphere: bool = True,
                 num_moons: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.has_atmosphere = has_atmosphere
        self.num_moons = num_moons

    def summary(self) -> str:
        atmo = "has atmosphere" if self.has_atmosphere else "no atmosphere"
        moons = f"{self.num_moons} moon(s)"
        lines = [
            f"\n  🪐  Planet: {self.name}",
            f"     {self.describe()}",
            f"     {self.gravitational_pull()}",
            f"     {self.orbit_info()}",
            f"     [Features] {atmo}, {moons}",
        ]
        return "\n".join(lines)


"""
A galaxy: a massive structure containing stars, gravity, and cosmic scale.
Inherits from → CelestialBody, GalacticStructure, GravitationalBody
"""

class Galaxy(CelestialBody, GalacticStructure, GravitationalBody):


    def __init__(self, galaxy_type: str = "Spiral", **kwargs):
        super().__init__(**kwargs)
        self.galaxy_type = galaxy_type

    def summary(self) -> str:
        lines = [
            f"\n  🌌  Galaxy: {self.name}  ({self.galaxy_type})",
            f"     {self.describe()}",
            f"     {self.galactic_info()}",
            f"     {self.gravitational_pull()}",
        ]
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════
#  3.  SPECIFIC OBJECTS
# ══════════════════════════════════════════════════════════

class Sun(Star):
    """Our star. Inherits the full Star chain."""

    def __init__(self):
        super().__init__(
            name="Sun",
            diameter_km=1_391_000,
            luminosity_suns=1.0,
            mass_kg=1.989e30,
            star_type="G-type (Yellow Dwarf)",
        )


class Earth(Planet):
    """Our home planet."""

    def __init__(self):
        super().__init__(
            name="Earth",
            diameter_km=12_742,
            mass_kg=5.972e24,
            orbital_period_days=365.25,
            orbital_radius_km=149_600_000,
            has_atmosphere=True,
            num_moons=1,
        )


class Mars(Planet):
    """The Red Planet."""

    def __init__(self):
        super().__init__(
            name="Mars",
            diameter_km=6_779,
            mass_kg=6.417e23,
            orbital_period_days=686.97,
            orbital_radius_km=227_900_000,
            has_atmosphere=True,
            num_moons=2,
        )


class Jupiter(Planet):
    """The largest planet in the Solar System."""

    def __init__(self):
        super().__init__(
            name="Jupiter",
            diameter_km=139_820,
            mass_kg=1.898e27,
            orbital_period_days=4_332.59,
            orbital_radius_km=778_500_000,
            has_atmosphere=True,
            num_moons=95,
        )


class MilkyWay(Galaxy):
    """Our home galaxy."""

    def __init__(self):
        super().__init__(
            name="Milky Way",
            diameter_km=9.461e17,           # ~100,000 light-years in km
            diameter_light_years=105_700,
            num_stars=2e11,                 # ~200 billion stars
            mass_kg=1.5e42,
            galaxy_type="Barred Spiral",
        )


# ══════════════════════════════════════════════════════════
#  4.  PRINT HELPERS
# ══════════════════════════════════════════════════════════

WIDTH = 60

def section(title: str):
    print()
    print("═" * WIDTH)
    print(f"  {title}")
    print("═" * WIDTH)

def show_mro(cls):
    """Print the Method Resolution Order for a class."""
    chain = " → ".join(c.__name__ for c in cls.__mro__)
    print(f"  MRO: {chain}")


# ══════════════════════════════════════════════════════════
#  5.  MAIN DEMO
# ══════════════════════════════════════════════════════════

def main():
    print()
    print("  🌠  Solar System — Multiple Inheritance Demo")
    print("  " + "─" * 56)

    # ── Create objects ────────────────────────────────────
    sun      = Sun()
    earth    = Earth()
    mars     = Mars()
    jupiter  = Jupiter()
    milkyway = MilkyWay()

    # ── Show class hierarchy (MRO) ────────────────────────
    section("Method Resolution Order (MRO)")
    print("  Python resolves inherited methods left-to-right,")
    print("  depth-first using the C3 linearisation algorithm.\n")
    for cls in [Sun, Earth, Mars, Jupiter, MilkyWay]:
        print(f"  {cls.__name__}")
        show_mro(cls)
        print()

    # ── Star ──────────────────────────────────────────────
    section("⭐  The Sun  —  Star")
    print(sun.summary())

    # ── Planets ───────────────────────────────────────────
    section("🪐  Planets  —  Planet (inherits CelestialBody + GravitationalBody + OrbitalBody)")
    for planet in [earth, mars, jupiter]:
        print(planet.summary())

    # ── Galaxy ────────────────────────────────────────────
    section("🌌  The Milky Way  —  Galaxy")
    print(milkyway.summary())

    # ── Polymorphism demo ─────────────────────────────────
    section("🔁  Polymorphism — all objects share describe()")
    print("  Every object inherits describe() from CelestialBody,\n"
          "  even though they also have other base classes:\n")
    for obj in [sun, earth, mars, jupiter, milkyway]:
        print(f"  {obj.describe()}")

    # ── isinstance checks ─────────────────────────────────
    section("🔍  isinstance() Checks")
    checks = [
        (sun,      Star,             "Sun is a Star"),
        (sun,      CelestialBody,    "Sun is a CelestialBody"),
        (sun,      Luminous,         "Sun is Luminous"),
        (sun,      GravitationalBody,"Sun is a GravitationalBody"),
        (earth,    Planet,           "Earth is a Planet"),
        (earth,    OrbitalBody,      "Earth is an OrbitalBody"),
        (earth,    Luminous,         "Earth is Luminous"),       # False — planets don't shine
        (milkyway, Galaxy,           "MilkyWay is a Galaxy"),
        (milkyway, GalacticStructure,"MilkyWay is a GalacticStructure"),
    ]
    for obj, cls, label in checks:
        result = isinstance(obj, cls)
        tick = "✅" if result else "❌"
        print(f"  {tick}  {label:<40} → {result}")

    print()
    print("═" * WIDTH)
    print("  Demo complete. 🚀")
    print("═" * WIDTH)
    print()




#
# Main Program
#



if __name__ == "__main__":
    main()


#
# End of Main Program
#
