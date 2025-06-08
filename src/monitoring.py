import time
import psutil
import GPUtil
from collections import defaultdict, deque
from datetime import datetime


class Metrics:
    
    def __init__(self):
        self.pipeline_executions = deque(maxlen=50)
        self.step_metrics = defaultdict(lambda: defaultdict(int))
        self.current_execution = None
        
    def start_execution(self, text):
        self.current_execution = {
            'text': text[:50] + "..." if len(text) > 50 else text,
            'start_time': time.time(),
            'steps': [],
            'status': 'running'
        }
    
    def record_step(self, step_name, duration, status='success'):
        if self.current_execution:
            self.current_execution['steps'].append({
                'name': step_name,
                'duration': duration,
                'status': status,
                'timestamp': time.time()
            })
            
            self.step_metrics[step_name]['total'] += 1
            self.step_metrics[step_name][status] += 1
    
    def finish_execution(self, status='success', error=None):
        if self.current_execution:
            self.current_execution['status'] = status
            self.current_execution['duration'] = time.time() - self.current_execution['start_time']
            self.current_execution['end_time'] = time.time()
            
            if error:
                self.current_execution['error'] = error
                
            self.pipeline_executions.append(self.current_execution.copy())
            self.current_execution = None
    
    def get_summary(self):
        executions = list(self.pipeline_executions)

        # Pipeline stats
        total = len(executions)
        successful = len([e for e in executions if e['status'] == 'success'])
        failed = total - successful
        success_rate = successful / total if total > 0 else 0
        pipeline_stats = {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': success_rate
        }
        
        # Step statistics
        step_stats = {}
        for step_name, stats in self.step_metrics.items():
            total_step = stats.get('total', 0)
            success_step = stats.get('success', 0)
            step_stats[step_name] = {
                'total': total_step,
                'success': success_step,
                'failure': stats.get('failure', 0),
                'success_rate': success_step / total_step if total_step > 0 else 0
            }
        
        # System metrics
        try:
            gpu_stats = GPUtil.getGPUs()
            gpu_usage = gpu_stats[0].load * 100 if gpu_stats else 0
            gpu_memory = gpu_stats[0].memoryUtil * 100 if gpu_stats else 0
        except:
            gpu_usage = 0
            gpu_memory = 0
            
        system_stats = {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'gpu_percent': gpu_usage,
            'gpu_memory_percent': gpu_memory
        }
        
        return {
            'pipeline_stats': pipeline_stats,
            'step_stats': step_stats,
            'system': system_stats
        }
    
    def get_execution_history(self):
        history = []
        for exec_data in self.pipeline_executions:
            history.append({
                'text': exec_data['text'],
                'status': exec_data['status'],
                'duration': exec_data.get('duration', 0),
                'timestamp': datetime.fromtimestamp(exec_data.get('end_time', exec_data['start_time'])),
                'steps': exec_data.get('steps', []),
                'error': exec_data.get('error')
            })
        return history
