from src.repositories.depot_repository import DepotRepository
from src.repositories.vehicle_repository import VehicleRepository
from src.algorithms.knapsack_optimizer import KnapsackOptimizer
from src.handlers.exceptions import CustomAPIException
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class SchedulerService:
    """
    Service Layer connecting repositories and the optimizer.
    Responsible for executing the core business workflow and generating standardized responses.
    """
    
    @staticmethod
    def generate_schedule(depot_id: int) -> dict:
        Log("backend", "info", "service", f"Scheduler optimization started for depot {depot_id}")
        
        try:
            # 1. Fetch Depot Data
            depot_data = DepotRepository.get_depot(depot_id)
            available_hours = depot_data.get("MechanicHours", 0)
            
            # Handle potential edge cases
            if available_hours <= 0:
                Log("backend", "warn", "service", f"Depot {depot_id} reported 0 available MechanicHours")
            
            # 2. Fetch ALL Vehicle Task Data
            tasks_data = VehicleRepository.get_all_tasks()
            
            # 3. Validate responses
            if not isinstance(tasks_data, list):
                Log("backend", "error", "service", "Invalid tasks format received from repository")
                raise CustomAPIException("Tasks data format is invalid")
                
            # 4. Run optimization algorithm
            optimization_result = KnapsackOptimizer.optimize(available_hours, tasks_data)
            
            # 5. Generate final response
            used_hours = optimization_result["usedHours"]
            remaining_hours = available_hours - used_hours
            
            final_response = {
                "depotId": depot_id,
                "availableHours": available_hours,
                "usedHours": used_hours,
                "remainingHours": remaining_hours,
                "totalImpact": optimization_result["totalImpact"],
                "selectedTasks": optimization_result["selectedTasks"]
            }
            
            Log("backend", "info", "service", f"Scheduler optimization completed for depot {depot_id}")
            return final_response
            
        except Exception as e:
            Log("backend", "error", "service", f"Scheduler service failed: {str(e)}")
            raise CustomAPIException(f"Failed to generate schedule: {str(e)}")
