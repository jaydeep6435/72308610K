from django.test import TestCase
from unittest.mock import patch
from src.repositories.depot_repository import DepotRepository
from src.handlers.exceptions import CustomAPIException

class RepositoryTests(TestCase):
    @patch('src.utils.http_client.http_client.get')
    def test_depot_repository_success(self, mock_get):
        mock_get.return_value = {"depots": [{"ID": 1, "MechanicHours": 60}]}
        
        data = DepotRepository.get_depot(1)
        self.assertEqual(data["MechanicHours"], 60)
        mock_get.assert_called_once()
        
    @patch('src.utils.http_client.http_client.get')
    def test_depot_repository_failure(self, mock_get):
        mock_get.side_effect = Exception("Network Error")
        
        with self.assertRaises(CustomAPIException):
            DepotRepository.get_depot(1)
