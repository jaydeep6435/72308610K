from django.test import TestCase
from unittest.mock import patch
from src.services.scheduler_service import SchedulerService
from src.handlers.exceptions import CustomAPIException

class ServiceTests(TestCase):
    @patch('src.algorithms.knapsack_optimizer.KnapsackOptimizer.optimize')
    @patch('src.repositories.vehicle_repository.VehicleRepository.get_all_tasks')
    @patch('src.repositories.depot_repository.DepotRepository.get_depot')
    def test_scheduler_service_success(self, mock_depot, mock_tasks, mock_opt):
        mock_depot.return_value = {"depotId": 1, "MechanicHours": 60}
        mock_tasks.return_value = [{"TaskID": "T1", "Duration": 20, "Impact": 100}]
        mock_opt.return_value = {
            "totalImpact": 100,
            "usedHours": 20,
            "selectedTasks": [{"TaskID": "T1", "Duration": 20, "Impact": 100}]
        }
        
        res = SchedulerService.generate_schedule(1)
        self.assertEqual(res["depotId"], 1)
        self.assertEqual(res["remainingHours"], 40)
        self.assertEqual(res["totalImpact"], 100)
        
    @patch('src.repositories.depot_repository.DepotRepository.get_depot')
    def test_scheduler_service_failure(self, mock_depot):
        mock_depot.side_effect = Exception("Database down")
        with self.assertRaises(CustomAPIException):
            SchedulerService.generate_schedule(1)
