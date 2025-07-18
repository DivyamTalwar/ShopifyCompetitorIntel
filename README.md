# Shopify Insights Fetcher

This application fetches insights from Shopify stores, including product catalogs, policies, and contact information. It also performs competitor analysis and saves all data to a MySQL database.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create a `.env` file** in the root directory and add the following environment variables:

    ```
    FIRECRRAWL_API_KEY="YOUR_FIRECRRAWL_API_KEY"
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    DATABASE_URL="mysql+pymysql://user:password@host/db_name"
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    GOOGLE_CSE_ID="YOUR_GOOGLE_CSE_ID"
    ```

    -   `FIRECRRAWL_API_KEY`: Your API key for the Firecrawl service.
    -   `GEMINI_API_KEY`: Your API key for the Google Generative AI service.
    -   `DATABASE_URL`: The connection string for your MySQL database.
    -   `GOOGLE_API_KEY`: Your API key for the Google Custom Search API.
    -   `GOOGLE_CSE_ID`: Your Custom Search Engine ID.

## Running the Application

Once the setup is complete, you can run the application with the following command:

```bash
uvicorn app.main:app --reload
