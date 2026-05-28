# MCP API Keys
BRIGHTDATA_API_KEY=
CONTEXT7_API_KEY=
AGENTQL_API_KEY=
BRAVE_SEARCH_API_KEY=

# CONFIGURED TOOLS LIST
MCP_BRIGHTDATA_ENABLED=true
MCP_SEQUENTIAL_THINKING_ENABLED=true
MCP_CONTEXT7_ENABLED=true
MCP_GIT_ENABLED=true
MCP_PUPPETEER_ENABLED=true
MCP_PLAYWRIGHT_ENABLED=true
MCP_AGENTQL_ENABLED=true
MCP_BRAVE_SEARCH_ENABLED=true
MCP_DEVTOOLS_MCP_ENABLED=true
MCP_SELENIUM_MCP_ENABLED=true

# AVAILABLE TOOLS LIST


  sequential-thinking - Ready ( 1 tool)
   Tools:
   - sequentialthinking
     A detailed tool for dynamic and reflective problem-solving through thoughts.
     This tool helps analyze problems through a flexible thinking process that can adapt and evolve.
     Each thought can build on, question, or revise previous insights as understanding deepens.

     When to use this tool:
     - Breaking down complex problems into steps
     - Planning and design with room for revision
     - Analysis that might need course correction
     - Problems where the full scope might not be clear initially
     - Problems that require a multi-step solution
     - Tasks that need to maintain context over multiple steps
     - Situations where irrelevant information needs to be filtered out

     Key features:
     - You can adjust total_thoughts up or down as you progress
     - You can question or revise previous thoughts
     - You can add more thoughts even after reaching what seemed like the end
     - You can express uncertainty and explore alternative approaches
     - Not every thought needs to build linearly - you can branch or backtrack
     - Generates a solution hypothesis
     - Verifies the hypothesis based on the Chain of Thought steps
     - Repeats the process until satisfied
     - Provides a correct answer

     Parameters explained:
     - thought: Your current thinking step, which can include:
     * Regular analytical steps
     * Revisions of previous thoughts
     * Questions about previous decisions
     * Realizations about needing more analysis
     * Changes in approach
     * Hypothesis generation
     * Hypothesis verification
     - next_thought_needed: True if you need more thinking, even if at what seemed like the end
     - thought_number: Current number in sequence (can go beyond initial total if needed)
     - total_thoughts: Current estimate of thoughts needed (can be adjusted up/down)
     - is_revision: A boolean indicating if this thought revises previous thinking
     - revises_thought: If is_revision is true, which thought number is being reconsidered
     - branch_from_thought: If branching, which thought number is the branching point
     - branch_id: Identifier for the current branch (if any)
     - needs_more_thoughts: If reaching end but realizing more thoughts needed

     You should:
     1. Start with an initial estimate of needed thoughts, but be ready to adjust
     2. Feel free to question or revise previous thoughts
     3. Don't hesitate to add more thoughts if needed, even at the "end"
     4. Express uncertainty when present
     5. Mark thoughts that revise previous thinking or branch into new paths
     6. Ignore information that is irrelevant to the current step
     7. Generate a solution hypothesis when appropriate
     8. Verify the hypothesis based on the Chain of Thought steps
     9. Repeat the process until satisfied with the solution
     10. Provide a single, ideally correct answer as the final output
     11. Only set next_thought_needed to false when truly done and a satisfactory answer is reached


 context7 - Ready ( 2 tools)
   Tools:
   - get-library-docs
     Fetches up-to-date documentation for a library. You must call 'resolve-library-id' first to obtain the exact Context7-compatible library ID required to use this 
       tool, UNLESS 
     the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.
   - resolve-library-id
     Resolves a package/product name to a Context7-compatible library ID and returns a list of matching libraries.

     You MUST call this function before 'get-library-docs' to obtain a valid Context7-compatible library ID UNLESS the user explicitly provides a library ID in the 
       format 
     '/org/project' or '/org/project/version' in their query.

     Selection Process:
     1. Analyze the query to understand what library/package the user is looking for
     2. Return the most relevant match based on:
     - Name similarity to the query (exact matches prioritized)
     - Description relevance to the query's intent
     - Documentation coverage (prioritize libraries with higher Code Snippet counts)
     - Trust score (consider libraries with scores of 7-10 more authoritative)

     Response Format:
     - Return the selected library ID in a clearly marked section
     - Provide a brief explanation for why this library was chosen
     - If multiple good matches exist, acknowledge this but proceed with the most relevant one
     - If no good matches exist, clearly state this and suggest query refinements

     For ambiguous queries, request clarification before proceeding with a best-guess match.


 git - Ready ( 12 tools)
   Tools:
   - git_add
     Adds file contents to the staging area
   - git_branch
     List Git branches
   - git_checkout
     Switches branches
   - git_commit
     Records changes to the repository
   - git_create_branch
     Creates a new branch from an optional base branch
   - git_diff
     Shows differences between branches or commits
   - git_diff_staged
     Shows changes that are staged for commit
   - git_diff_unstaged
     Shows changes in the working directory that are not yet staged
   - git_log
     Shows the commit logs
   - git_reset
     Unstages all staged changes
   - git_show
     Shows the contents of a commit
   - git_status
     Shows the working tree status


 puppeteer - Ready ( 7 tools)
   Tools:
   - puppeteer_click
     Click an element on the page
   - puppeteer_evaluate
     Execute JavaScript in the browser console
   - puppeteer_fill
     Fill out an input field
   - puppeteer_hover
     Hover an element on the page
   - puppeteer_navigate
     Navigate to a URL
   - puppeteer_screenshot
     Take a screenshot of the current page or a specific element
   - puppeteer_select
     Select an element on the page with Select tag


 playwright - Ready ( 21 tools)
  Tools:
  - browser_click
    Perform click on a web page
  - browser_close
    Close the page
  - browser_console_messages
    Returns all console messages
  - browser_drag
    Perform drag and drop between two elements
  - browser_evaluate
    Evaluate JavaScript expression on page or element
  - browser_file_upload
    Upload one or multiple files
  - browser_fill_form
    Fill multiple form fields
  - browser_handle_dialog
    Handle a dialog
  - browser_hover
    Hover over element on page
  - browser_install
    Install the browser specified in the config. Call this if you get an error about the browser not being installed.
  - browser_navigate
    Navigate to a URL
  - browser_navigate_back
    Go back to the previous page
  - browser_network_requests
    Returns all network requests since loading the page
  - browser_press_key
    Press a key on the keyboard
  - browser_resize
    Resize the browser window
  - browser_select_option
    Select an option in a dropdown
  - browser_snapshot
    Capture accessibility snapshot of the current page, this is better than screenshot
  - browser_tabs
    List, create, close, or select a browser tab.
  - browser_take_screenshot
    Take a screenshot of the current page. You can't perform actions based on the screenshot, use browser_snapshot for actions.
  - browser_type
    Type text into editable element
  - browser_wait_for
    Wait for text to appear or disappear or a specified time to pass


 agentql - Ready ( 1 tool)
   Tools:
   - extract-web-data
     Extracts structured data as JSON from a web page given a URL using a Natural Language description of the data.


 brave-search - Ready ( 2 tools)
   Tools:
   - brave_local_search
     Searches for local businesses and places using Brave's Local Search API. Best for queries related to physical locations, businesses, restaurants, services, etc. 
       Returns 
     detailed information including:
     - Business names and addresses
     - Ratings and review counts
     - Phone numbers and opening hours
     Use this when the query implies 'near me' or mentions specific locations. Automatically falls back to web search if no local results are found.
   - brave_web_search
     Performs a web search using the Brave Search API, ideal for general queries, news, articles, and online content. Use this for broad information gathering, recent
       events, or
     when you need diverse web sources. Supports pagination, content filtering, and freshness controls. Maximum 20 results per request, with offset for pagination.


 devtools_mcp - Ready ( 26 tools)
   Tools:
   - click
     Clicks on the provided element
   - close_page
     Closes the page by its index. The last open page cannot be closed.
   - drag
     Drag an element onto another element
   - emulate_cpu
     Emulates CPU throttling by slowing down the selected page's execution.
   - emulate_network
     Emulates network conditions such as throttling or offline mode on the selected page.
   - evaluate_script
     Evaluate a JavaScript function inside the currently selected page. Returns the response as JSON
     so returned values have to JSON-serializable.
   - fill
     Type text into a input, text area or select an option from a <select> element.
   - fill_form
     Fill out multiple form elements at once
   - get_network_request
     Gets a network request by URL. You can get all requests by calling list_network_requests.
   - handle_dialog
     If a browser dialog was opened, use this command to handle it
   - devtools_mcp__hover
     Hover over the provided element
   - list_console_messages
     List all console messages for the currently selected page since the last navigation.
   - list_network_requests
     List all requests for the currently selected page since the last navigation.
   - list_pages
     Get a list of pages open in the browser.
   - navigate_page
     Navigates the currently selected page to a URL.
   - navigate_page_history
     Navigates the currently selected page.
   - new_page
     Creates a new page
   - performance_analyze_insight
     Provides more detailed information on a specific Performance Insight that was highlighted in the results of a trace recording.
   - performance_start_trace
     Starts a performance trace recording on the selected page. This can be used to look for performance problems and insights to improve the performance of the page.
       It will also
     report Core Web Vital (CWV) scores for the page.
   - performance_stop_trace
     Stops the active performance trace recording on the selected page.
   - resize_page
     Resizes the selected page's window so that the page has specified dimension
   - select_page
     Select a page as a context for future tool calls.
   - devtools_mcp__take_screenshot
     Take a screenshot of the page or element.
   - take_snapshot
     Take a text snapshot of the currently selected page. The snapshot lists page elements along with a unique
     identifier (uid). Always use the latest snapshot. Prefer taking a snapshot over taking a screenshot.
   - devtools_mcp__upload_file
     Upload a file through a provided element.
   - wait_for
     Wait for the specified text to appear on the selected page.


 selenium_mcp - Ready ( 14 tools)
   Tools:
   - click_element
     clicks an element
   - close_session
     closes the current browser session
   - double_click
     performs a double click on an element
   - drag_and_drop
     drags an element and drops it onto another element
   - find_element
     finds an element
   - get_element_text
     gets the text() of an element
   - hover
     moves the mouse to hover over an element
   - navigate
     navigates to a URL
   - press_key
     simulates pressing a keyboard key
   - right_click
     performs a right click (context click) on an element
   - send_keys
     sends keys to an element, aka typing
   - start_browser
     launches browser
   - take_screenshot
     captures a screenshot of the current page
   - upload_file
     uploads a file using a file input element