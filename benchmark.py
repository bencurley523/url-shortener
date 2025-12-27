import asyncio
import aiohttp
import time

# CONFIGURATION
URL = "http://localhost:8000/google" # Make sure this short code exists!
TOTAL_REQUESTS = 2000
CONCURRENT_USERS = 50

async def fetch(session):
    async with session.get(URL, allow_redirects=False) as response:
        await response.read()
        return response.status

async def main():
    print(f"🚀 Starting Load Test: {TOTAL_REQUESTS} requests with {CONCURRENT_USERS} concurrent users...")
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        
        tasks = []
        for _ in range(TOTAL_REQUESTS):
            tasks.append(fetch(session))
            
            # Simple batching to maintain concurrency
            if len(tasks) >= CONCURRENT_USERS:
                await asyncio.gather(*tasks)
                tasks = []
        
        # Finish remaining
        if tasks:
            await asyncio.gather(*tasks)
            
        end_time = time.time()
        
    duration = end_time - start_time
    rps = TOTAL_REQUESTS / duration
    
    print(f"\n📊 RESULTS:")
    print(f"---------------------------")
    print(f"Time Taken: {duration:.2f} seconds")
    print(f"RPS:        {rps:.2f} requests/second")
    print(f"---------------------------")

if __name__ == "__main__":
    # Create the short link first manually if it doesn't exist!
    asyncio.run(main())