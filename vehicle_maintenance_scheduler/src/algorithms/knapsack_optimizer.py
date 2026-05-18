import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class KnapsackOptimizer:
    """
    0/1 Knapsack Optimization for Vehicle Maintenance Scheduling.
    
    Time Complexity: O(n * W)
    Space Complexity: O(n * W)
    Where n is the number of tasks and W is the available mechanic hours.
    Memory optimization achieved using 2D DP array. Further space optimization 
    to O(W) is possible but requires a separate approach for reconstruction.
    """
    
    @staticmethod
    def optimize(available_hours: int, tasks: list) -> dict:
        Log("backend", "info", "utils", "Optimization algorithm started")
        
        if not tasks:
            Log("backend", "warn", "utils", "Invalid inputs: empty task list provided")
            return {
                "totalImpact": 0,
                "usedHours": 0,
                "selectedTasks": []
            }
            
        n = len(tasks)
        W = available_hours
        
        if W <= 0:
            Log("backend", "warn", "utils", "Edge-case detection: Invalid or zero available hours")
            return {
                "totalImpact": 0,
                "usedHours": 0,
                "selectedTasks": []
            }
            
        # Initialize DP table (n+1 x W+1)
        dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
        
        # Build DP table
        for i in range(1, n + 1):
            task = tasks[i - 1]
            wt = task.get("Duration", 0)
            val = task.get("Impact", 0)
            
            # Skip invalid tasks
            if wt <= 0 or val < 0:
                Log("backend", "warn", "utils", f"Edge-case detection: Skipping invalid task {task.get('TaskID')}")
                for w in range(W + 1):
                    dp[i][w] = dp[i - 1][w]
                continue
                
            for w in range(1, W + 1):
                if wt <= w:
                    dp[i][w] = max(val + dp[i - 1][w - wt], dp[i - 1][w])
                else:
                    dp[i][w] = dp[i - 1][w]
                    
        Log("backend", "debug", "utils", "DP execution milestones reached")
        
        # Reconstruction logic
        res = dp[n][W]
        total_impact = res
        w = W
        selected_tasks = []
        used_hours = 0
        
        for i in range(n, 0, -1):
            if res <= 0:
                break
            
            # Either the result comes from the top (dp[i-1][w]) or from (val + dp[i-1][w-wt])
            if res == dp[i - 1][w]:
                continue
            else:
                task = tasks[i - 1]
                selected_tasks.append(task)
                
                wt = task.get("Duration", 0)
                val = task.get("Impact", 0)
                
                used_hours += wt
                res -= val
                w -= wt
                
        # To maintain the natural sequence (though not strictly required)
        selected_tasks.reverse()
        
        Log("backend", "info", "utils", "Optimization generation completed")
        
        return {
            "totalImpact": total_impact,
            "usedHours": used_hours,
            "selectedTasks": selected_tasks
        }
