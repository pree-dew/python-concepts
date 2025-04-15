import os
import asyncio
import functools
from concurrent.futures import ProcessPoolExecutor


class MapReducer:
    def __init__(self, input_dir, output_dir, workers, sample_size, map_func, reduce_func):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.workers = workers
        self.sample_size = sample_size
        self.map_func = map_func
        self.reduce_func = reduce_func

    def partition_data(self, sample_size):
        """
        Sample log lines from the input directory.
        
        Returns:
            A list of sampled log lines.
        """
        log_lines = []

        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith('.log'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        # read the file line by line
                        for line in f:
                            log_lines.append(line.strip())

                            # If we have enough lines, yield them
                            if len(log_lines) >= sample_size:
                                yield log_lines[:sample_size]
                                log_lines = log_lines[sample_size:]

        # If there are remaining lines, yield them
        if log_lines:
            yield log_lines

    def run_map_phase(self, chunk):
        """
        Run the map phase of the MapReduce job.
        
        Args:
            chunk: A chunk of log lines to process.
        
        Returns:
            A list of processed log lines.
        """
        processed_data = []
        for line in chunk:
            result = self.map_func(line)
            if result:
                map_result = {}
                for k, v in result.items():
                    if k not in map_result:
                        map_result[k] = dict()
                    if v not in map_result[k]:
                        map_result[k][v] = 0

                    map_result[k][v] += 1
                processed_data.append(map_result)
                        
        
        return processed_data

    async def run_reduce_phase(self, chunk_size, loop, executor, processed_dicts):
        """
        Run the reduce phase of the MapReduce job.
        
        Args:
            chunk: A chunk of processed log lines to reduce.
        
        Returns:
            A list of reduced log lines.
        """
        chunks = processed_dicts[:chunk_size]
        tasks = []
        while len(chunks) > 0:
            # Create a task to merge multiple chunks together
            tasks.append(loop.run_in_executor(
                executor, 
                functools.partial(
                    # Change is here - we're passing chunks (list of dicts) instead of a single chunk
                    functools.reduce, 
                    self.reduce_func, 
                    chunks
                )
            ))
            
            reduced_data = await asyncio.gather(*tasks)
            # check if reduced_data is equal to the processed_dicts
            if reduced_data == processed_dicts:
                break
            processed_dicts = processed_dicts[chunk_size:]
            processed_dicts.extend(reduced_data)
            chunks = processed_dicts[:chunk_size]
            tasks = []  # Reset tasks for the next iteration

        return processed_dicts

    async def run_analysis(self):
        """
        Run the map phase of the MapReduce job.
        """
        
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            tasks = []
            for chunk in self.partition_data(self.sample_size):
                tasks.append(loop.run_in_executor(executor, functools.partial(self.run_map_phase, chunk)))

            processed_data = await asyncio.gather(*tasks)

            reduced_data = await self.run_reduce_phase(100, loop, executor, processed_data[0])
            return reduced_data



async def run_mapreduce_job(input_dir, output_dir, workers=4, sample_size=10000, map_func=None, reduce_func=None):
    """
    Run the MapReduce job for log analysis.
    
    Args:
        input_dir: Directory containing log files
        output_dir: Directory to save the output
        workers: Number of worker processes to use
        sample_size: Number of log lines to sample for pattern discovery
    """
    
    map_reducer = MapReducer(input_dir, output_dir, workers, sample_size, map_func, reduce_func)
    return await map_reducer.run_analysis()

        
        
