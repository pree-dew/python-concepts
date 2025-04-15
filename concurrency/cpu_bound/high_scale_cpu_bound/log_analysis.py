import os
import json
import random
import logging
import argparse
import asyncio

from pattern_discovery import LogPatternDiscovery
from mapreduce import run_mapreduce_job

# Configure logging
logger = logging.getLogger('log_analyzer')

class LogAnalyzer:
    def __init__(self, input_dir, output_dir, sample_size=10000, workers=None):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.sample_size = sample_size
        self.workers = workers or os.cpu_count()
        self.mapper_func = None
        self.reducer_func = None

        self.pattern_discovery = LogPatternDiscovery(sample_size=self.sample_size)
        self.logger = logger

    async def run_analysis(self):
        try:
            await self._discover_patterns()

            processed_data = await run_mapreduce_job(
                input_dir=self.input_dir,
                output_dir=self.output_dir,
                workers=self.workers,
                sample_size=self.sample_size,
                map_func=self.mapper_func,
                reduce_func=self.reducer_func
            )

            return True, processed_data
        except Exception as e:
            self.logger.error(f"An error occurred during analysis: {e}")
            return False, None

    async def _sample_logs(self):
        # Sample log lines from the input directory
        log_lines = []

        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith('.log'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        log_lines.extend(lines)

        # Randomly sample log lines
        sampled_lines = random.sample(log_lines, min(self.sample_size, len(log_lines)))
        
        return sampled_lines

    async def _discover_patterns(self):
        # Discover patterns in the sampled log lines
        
        # pick a random sample of log lines
        #log_lines = await self._sample_logs()
        # Not implementing the pattern detection for simplicity and considering
        # standard logs

        self.mapper_func = self.pattern_discovery.get_mapper_function()
        self.reducer_func = self.pattern_discovery.get_reducer_function()


    async def _generate_report(self):
        # Generate a report based on the discovered patterns
        pass




async def main():
    parser = argparse.ArgumentParser(description='Petabyte-scale log analysis using custom MapReduce')
    parser.add_argument('--input', '-i', required=True, help='Input directory containing log files')
    parser.add_argument('--output', '-o', required=True, help='Output directory for analysis results')
    parser.add_argument('--sample', '-s', type=int, default=10000, help='Number of log lines to sample for pattern discovery')
    parser.add_argument('--workers', '-w', type=int, default=None, help='Number of worker processes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Run analysis
    analyzer = LogAnalyzer(
        input_dir=args.input,
        output_dir=args.output,
        sample_size=args.sample,
        workers=args.workers
    )

    success, processed_data = await analyzer.run_analysis()

    if success:
        logger.info(f"Analysis complete. Results are available in {args.output}")
        # save processed data to output directory
        output_file = os.path.join(args.output, 'processed_data.json')
        with open(output_file, 'w') as f:
            json.dump(processed_data, f, indent=4)
        return 0
    else:
        logger.error("Analysis failed")
        return 1


if __name__ == "__main__":
    asyncio.run(main())
                                              
