import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from quart import Quart, jsonify
from quart_cors import cors
import time

app = Quart(__name__)
cors(app)

async def fetch_items(page, page_number, retries=3):
    url = f'https://traderie.com/royalehigh/products?page={page_number}'
    
    items = []
    print(f"Attempting to fetch page {page_number}")

    for attempt in range(retries):
        try:
            await page.goto(url, timeout=60000)  # Increase timeout to 60 seconds
            
            # Check for no results message before waiting for item containers
            no_results_message = await page.query_selector('.no-items')
            if no_results_message:
                no_results_text = await no_results_message.inner_text()
                if "No results could be found" in no_results_text:
                    print(f"No more results starting from page {page_number}. Stopping.")
                    return items  # Return collected items even if no more items are found

            # Wait for the specific element to load
            try:
                await page.wait_for_selector('.sc-eqUAAy.sc-SrznA.cZMYZT.WYSac.item-img-container', timeout=15000)
            except PlaywrightTimeoutError:
                print(f"TimeoutError: Page.wait_for_selector timed out on page {page_number}")
                continue  # Retry if timeout occurs

            # Extract items
            item_containers = await page.query_selector_all('.sc-eqUAAy.sc-SrznA.cZMYZT.WYSac.item-img-container')
            if not item_containers:
                print(f"No item containers found on page {page_number}")
            else:
                for container in item_containers:
                    try:
                        name_container = await container.query_selector('.sc-czkgLR.fsFCnf')
                        item_name = await name_container.inner_text()
                    except:
                        item_name = "Unknown"
                    try:
                        value_container = await container.query_selector('.listing-bells')
                        item_value = int((await value_container.inner_text()).replace(',', ''))
                    except:
                        item_value = 0
                    items.append({"name": item_name, "value": item_value})

            print(f"Page {page_number}: Found {len(items)} items")
            return items

        except PlaywrightTimeoutError as e:
            print(f"TimeoutError: {e} on page {page_number}")
            if attempt == retries - 1:
                print(f"Failed to fetch page {page_number} after {retries} attempts")

        except Exception as e:
            # Retry logic for network-related errors
            if 'net::ERR_NETWORK_CHANGED' in str(e):
                print(f"Network error on page {page_number}: {e}. Retrying... ({attempt + 1}/{retries})")
                if attempt == retries - 1:
                    print(f"Failed to fetch page {page_number} due to network error after {retries} attempts")
            else:
                print(f"Exception: {e} on page {page_number}")
                break

    return []

async def staggered_scrape_pages(start_page, batch_size=5, delay=1):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        all_items = []
        page_number = start_page
        active_tasks = []
        semaphore = asyncio.Semaphore(batch_size)  # Control concurrency

        # Cancellation flag
        cancel_flag = asyncio.Event()

        async def fetch_with_semaphore(page_number):
            async with semaphore:
                if cancel_flag.is_set():
                    return  # Exit early if cancellation is triggered
                try:
                    items = await fetch_items(page, page_number)
                    if items:
                        all_items.extend(items)
                    elif not cancel_flag.is_set():
                        cancel_flag.set()  # Set flag to stop fetching new pages if no items are found
                except asyncio.CancelledError:
                    print(f"Task for page {page_number} was cancelled.")
                await asyncio.sleep(delay)  # Staggered delay

        async def manage_tasks():
            nonlocal page_number
            while True:
                if len(active_tasks) < batch_size and not cancel_flag.is_set():
                    task = asyncio.create_task(fetch_with_semaphore(page_number))
                    active_tasks.append(task)
                    page_number += 1

                # Await completion of the first batch tasks and manage the list of active tasks
                done, pending = await asyncio.wait(active_tasks, return_when=asyncio.FIRST_COMPLETED)

                # Cancel the remaining tasks if no more pages need to be fetched
                if not pending and cancel_flag.is_set():
                    print(f"No more items found starting from page {start_page}. Stopping.")
                    break

                # Remove completed tasks from the active tasks list
                active_tasks[:] = [task for task in pending if not task.done()]

        try:
            await manage_tasks()
        finally:
            # Ensure all tasks are cancelled and the browser is closed
            for task in active_tasks:
                task.cancel()
            await browser.close()

        return all_items

@app.route('/items', methods=['GET'])
async def get_items():
    start_time = time.time()
    batch_size = 15  # Number of concurrent requests
    delay = 0.03  # Delay between requests
    all_items = await staggered_scrape_pages(0, batch_size, delay)  # Start scraping from page 0
    elapsed_time = time.time() - start_time
    print(f"Scraped {len(all_items)} items in {elapsed_time:.2f} seconds")
    return jsonify(all_items)

if __name__ == '__main__':
    app.run(debug=True)
