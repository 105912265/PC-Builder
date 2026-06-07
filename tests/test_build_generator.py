import unittest

from components.cpu import CPU
from components.gpu import GPU
from components.motherboard import Motherboard
from components.psu import PSU
from components.ram import RAM
from components.storage import Storage
from src.build_generator import generate_compatible_builds


class BuildGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU("CPU", 100, 0, 0, 100, 0.0, 4, "AM4")
        self.gpu = GPU("GPU", 200, 0, 0, 200, 0.0)
        self.motherboard = Motherboard("MOBO", 50, 10, "AM4", "DDR4")
        self.ram = RAM("RAM", 30, 5, 16, "DDR4")
        self.storage = Storage("SSD", 20, 5, 500, "NVMe")
        self.psu = PSU("PSU", 40, 550, "80+ Bronze")

    def test_returns_compatible_builds_with_limit(self):
        builds = generate_compatible_builds(
            [self.cpu],
            [self.gpu],
            [self.motherboard],
            [self.ram],
            [self.storage],
            [self.psu],
            budget=500,
            max_builds=5,
        )

        self.assertEqual(len(builds), 1)
        self.assertEqual(builds[0].components[0], self.cpu)

    def test_returns_no_builds_when_budget_is_too_low(self):
        builds = generate_compatible_builds(
            [self.cpu],
            [self.gpu],
            [self.motherboard],
            [self.ram],
            [self.storage],
            [self.psu],
            budget=100,
            max_builds=5,
        )

        self.assertEqual(builds, [])


if __name__ == "__main__":
    unittest.main()
