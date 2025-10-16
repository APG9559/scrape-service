from fastapi import FastAPI, Request
from pydantic import BaseModel
from firecrawl import FirecrawlApp
import os, re, time
from fastapi.middleware.cors import CORSMiddleware



# Initialize FastAPI
app = FastAPI(title="Job Scraper API", description="Scrapes job data from multiple portals using Firecrawl")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # List of allowed origins
    allow_credentials=True,           # Allow cookies/auth headers
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)

# Initialize Firecrawl
app_fc = FirecrawlApp(api_key="fc-4b7fd5a389f74250a05de6f372f4be9a")


# Define request body schema
class ScrapeRequest(BaseModel):
    urls: list[str]


@app.post("/scrape_jobs")
async def scrape_jobs():
    """Start scraping job portals and return raw HTML snippets."""
    # urls = req.urls

    print(f"🚀 Starting scrape for URLs...")

    # try:
    #     # Start Firecrawl batch job
    #     batch_scrape_job = app_fc.start_batch_scrape(urls=urls, formats=["html"])
    #     job_id = batch_scrape_job.id

    #     # Poll for completion
    #     while True:
    #         status = app_fc.get_batch_scrape_status(job_id)
    #         if status.status == "completed":
    #             break
    #         elif status.status in ["failed", "error"]:
    #             return {"status": "failed", "error": "Batch scrape job failed."}
    #         time.sleep(5)

    #     # Prepare results
    #     results = []
    #     for result in status.data:
    #         if result.metadata and result.html:
    #             url = result.metadata.source_url
    #             clean_name = re.sub(r"[^a-zA-Z0-9_-]", "_", url)
    #             filename = f"{clean_name}.html"
    #             results.append({
    #                 "url": url,
    #                 "file_name": filename,
    #                 "html_snippet": result.html[:1000]  # limited preview
    #             })

    #     return {
    #         "status": "success",
    #         "total_results": len(results),
    #         "results": results
    #     }

    # except Exception as e:
    #     return {"status": "error", "message": str(e)}
    # app = FirecrawlApp(api_key='fc-4b7fd5a389f74250a05de6f372f4be9a')

    # A list of URLs you want to scrape for job data
    urls_to_scrape = [
        # 'https://www.naukri.com/it-jobs?src=gnbjobs_homepage_srch',
        'https://m.timesjobs.com/mobile/jobs-search-result.html?jobsSearchCriteria=Information%20Technology&cboPresFuncArea=35',
        # 'https://www.linkedin.com/jobs/search?keywords=Software%20Developer',
        # 'https://in.indeed.com/jobs?q=fresher&l=Pune%2C+Maharashtra&from=searchOnHP%2CsearchSuggestions%2CwhatautocompleteSourceStandard%2Cwhereautocomplete&vjk=716a4d5e935de57b'
        # Add more job site URLs here
    ]

    print("🚀 Starting batch scrape job...")
    # Start the batch scrape job. You can request 'markdown', 'html', or both.
    batch_scrape_job = app_fc.start_batch_scrape(
        urls=urls_to_scrape,
        # Let's get the raw HTML to have all data available
        formats=['html'] 
    )

    print(f"Job started with ID: {batch_scrape_job.id}")

    job_id = batch_scrape_job.id

    # Poll for the job status until it's completed
    while True:
        batch_scrape_status = app_fc.get_batch_scrape_status(job_id)
        print(f"Checking job status... Current status: '{batch_scrape_status.status}'")
        if batch_scrape_status.status == 'completed':
            print("✅ Job completed successfully!")
            break
        elif batch_scrape_status.status in ['failed', 'error']:
            print(f"❌ Job failed with status: {batch_scrape_status.status}")
            exit() # Exit the script if the job fails
        time.sleep(5) # Wait for 5 seconds before checking again
        
    return batch_scrape_status.data
    # --- Save the results to files ---
    # Ensure there is data to process
    # if batch_scrape_status.data:
    #     # Create a directory to store the scraped data if it doesn't exist
    #     output_dir = "scraped_jobs_data"
    #     os.makedirs(output_dir, exist_ok=True)

    #     # Loop through each result in the completed job
    #     for result in batch_scrape_status.data:
    #         # The Document object has different attribute names
    #         # Use metadata and source properties instead
    #         if result.metadata and result.html:
    #             # Sanitize the URL to create a valid filename
    #             url = result.metadata.source_url  # Changed from result.source_url
    #             filename = re.sub(r'https?://', '', url)
    #             filename = re.sub(r'[^a-zA-Z0-9_-]', '_', filename) + ".html"
                
    #             # Define the full file path
    #             file_path = os.path.join(output_dir, filename)
                
    #             # Write the HTML content to the file
    #             try:
    #                 with open(file_path, 'w', encoding='utf-8') as f:
    #                     f.write(result.html)
    #                 print(f"Successfully saved data from {url} to {file_path}")
    #             except Exception as e:
    #                 print(f"Could not save file for {url}. Error: {e}")
    #         else:
    #             print(f"Failed to scrape data for URL. Missing required data.")

    # else:
    #     print("No data was returned from the batch scrape job.")
