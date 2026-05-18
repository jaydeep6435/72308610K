from django.test import TestCase
from src.algorithms.knapsack_optimizer import KnapsackOptimizer

class OptimizerTests(TestCase):
    def test_optimization_logic(self):
        tasks = [
            {"TaskID": "T1", "Duration": 10, "Impact": 50},
            {"TaskID": "T2", "Duration": 20, "Impact": 120},
            {"TaskID": "T3", "Duration": 30, "Impact": 150}
        ]
        
        # W = 40. 
        # Combinations: 
        # T1+T3: Duration=40, Impact=200 (Best)
        # T2+T3: Duration=50 > 40
        # T1+T2: Duration=30, Impact=170
        res = KnapsackOptimizer.optimize(40, tasks)
        self.assertEqual(res["totalImpact"], 200)
        self.assertEqual(res["usedHours"], 40)
        self.assertEqual(len(res["selectedTasks"]), 2)
        
    def test_invalid_capacity(self):
        tasks = [{"TaskID": "T1", "Duration": 10, "Impact": 50}]
        res = KnapsackOptimizer.optimize(0, tasks)
        self.assertEqual(res["totalImpact"], 0)
        self.assertEqual(len(res["selectedTasks"]), 0)
        
    def test_invalid_task_durations(self):
        # Negative duration shouldn't break the system, handled gracefully
        tasks = [{"TaskID": "T1", "Duration": -5, "Impact": 50}]
        res = KnapsackOptimizer.optimize(10, tasks)
        self.assertEqual(res["totalImpact"], 0)
