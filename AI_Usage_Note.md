# AI Usage Note — Fulfillment Hub

## Which AI tools I used and how

I used Claude (Anthropic) as a technical mentor throughout this project. I'm comfortable with Python, Pandas, SQL, and data analysis, but had never built or deployed a full application before, so I used Claude to explain unfamiliar tools and walk me through steps — not to make decisions for me. Every choice about what to build, what to prioritize, and when something needed to be redone was mine; Claude's role was to explain how to execute those choices and to troubleshoot errors as they came up (file path issues, a Git authentication prompt, a double-sidebar bug, a raw-HTML rendering bug, and a few file-naming mistakes along the way).

I directed the build in stages — reviewing each page as it was built, testing it myself in the browser, and asking for specific changes before moving forward, rather than accepting the first version of anything.

## Where I disagreed with or changed an AI suggestion

**1. Tooling choice (VS Code vs. Notepad + cmd).**
Partway through, Claude suggested switching to VS Code since it has a built-in terminal. I decided against it — I didn't want to learn a new tool under a tight deadline while I was already making progress with Notepad and Command Prompt, so I asked to continue with that setup instead. We completed the entire project without VS Code.

**2. Scope of the "wrong item shipped" problem.**
The brief mentions wrong products/variants sometimes being shipped. Claude's first suggestion was to only acknowledge this gap verbally in my video, to save build time. I felt that was too thin for something explicitly listed as a business problem, so I asked for a small, honest feature instead — a reminder on the Order Details page that prompts a double-check of the product and variant when an order reaches the Picking stage. I deliberately chose a middle ground: not a full solution, which would need barcode scanning, but more than just a spoken acknowledgment.

**3. Home page design and layout.**
The first version of the home page Claude gave me was functional but plain — default Streamlit styling, no custom font, and the feature cards weren't even clickable. I wasn't satisfied with that, since the brief specifically asked for something that feels like a real operational tool, not a generic auto-generated layout. I pushed back multiple times and asked for a better font, a cleaner card-based layout, and for the Dashboard/Orders/Inventory/Order Details cards to actually work as navigation links instead of just being decorative text. I went through three rounds of revisions on this page alone before I was satisfied with how it looked and functioned.

## What I decided and did myself

- Chose which two problems to prioritize most deeply — priority/delay visibility and inventory-driven blocking — based on my own judgment of which issues in the brief were most measurable and data-driven, and which would have the most real operational impact.
- Decided to fold Shipping/Staging information into the existing Order Details and Dashboard pages rather than building a 5th standalone page, to keep the app focused rather than padded with a thin extra page.
- Tested and verified the app's logic myself at each stage — for example, I specifically checked that marking an order as shipped actually reduced the Dashboard's Pending Orders count in real time, rather than assuming the numbers were correctly wired up.
- Made all the actual decisions during setup and deployment — creating accounts, approving GitHub authentication, choosing the repository name and app URL, and testing the live deployed link myself before considering it done.