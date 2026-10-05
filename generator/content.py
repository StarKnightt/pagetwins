"""Original copy for the ten base landing pages.

Every brand, person, company, quote and statistic below is fictional and was
written for this dataset. Each base page also carries the exact edit used for
each of its one-defect twins and its harmless control variant, so every twin
is reproducible from this file.
"""

LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua."
)

BASES = [
    # ------------------------------------------------------------------ B01
    dict(
        id="B01",
        brand="Tallyhawk",
        template="split",
        kind="SaaS",
        theme=dict(
            primary="#4F46E5", primary_ink="#FFFFFF", accent="#EEF2FF",
            bg="#FFFFFF", hero_bg="#FFFFFF", surface="#F7F8FC", text="#0F172A",
            muted="#4B5567", border="#E3E6EF", band_bg="#1E1B4B", band_ink="#FFFFFF",
            font_head='"Segoe UI", system-ui, sans-serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="14px", mark="hawk",
        ),
        title="Tallyhawk · Invoicing for freelancers",
        nav_links=["Features", "Pricing", "Customers"],
        nav_cta="Start free",
        hero=dict(
            eyebrow="Invoicing for freelancers and small studios",
            headline="Send invoices that get paid in days, not months",
            subhead=(
                "Tallyhawk turns your tracked hours into a clean invoice in one "
                "click, sends polite reminders for you, and lets clients pay by "
                "card or bank transfer."
            ),
            cta="Start free trial",
            cta2="See how it works",
            note="Free for up to 3 clients · No credit card needed",
            price_line=None,
            image_alt="Tallyhawk dashboard showing paid and overdue invoices",
            art="invoices",
        ),
        proof=dict(
            label="Trusted by 2,000+ freelancers and studios",
            logos=["Kestrel & Co", "Bluefern Studio", "Halcyon", "Orbitline", "Marrow Works"],
        ),
        features=dict(
            title="Everything between job done and money in",
            items=[
                ("One-click invoices",
                 "Pull tracked hours and expenses into a branded invoice. Edit any line before it goes out."),
                ("Reminders that sound like you",
                 "Tallyhawk nudges late clients on a schedule you set, in your own words, so you never have to chase."),
                ("Get paid your way",
                 "Clients pay by card or bank transfer straight from the invoice. Money lands in 2 business days."),
            ],
        ),
        testimonial=dict(
            quote=(
                "I used to spend Friday afternoons chasing payments. Now the "
                "reminders go out on their own and most clients pay within a week."
            ),
            name="Priya Raman",
            role="Brand designer, Raman Studio",
        ),
        pricing=dict(
            title="Simple pricing that grows with you",
            tiers=[
                dict(name="Free", price="$0", period="/month",
                     features=["Up to 3 clients", "Unlimited invoices", "Card payments"], cta="Start free"),
                dict(name="Pro", price="$12", period="/month", popular=True,
                     features=["Unlimited clients", "Automatic reminders", "Custom branding"], cta="Start free trial"),
                dict(name="Studio", price="$29", period="/month",
                     features=["Up to 5 team members", "Shared client list", "Priority support"], cta="Start free trial"),
            ],
            note="Prices in USD. Card payments carry a standard processing fee.",
        ),
        faq=[
            ("Is there a free plan?", "Yes. The Free plan covers up to 3 clients with no time limit."),
            ("Can I cancel anytime?", "Yes. Cancel from your settings and you will not be charged again."),
        ],
        band=dict(title="Spend Friday on work, not on chasing invoices", cta="Start free trial"),
        footer=dict(company="Tallyhawk Inc.", place="Made in Portland, Oregon"),
        defects=dict(
            typos=[("headline", "invoices", "invoces"), ("headline", "months", "montsh"),
                   ("subhead", "reminders", "remiders")],
            contradiction=dict(
                field="hero.note",
                value="Free for unlimited clients, forever · No credit card needed",
                conflicts_with="Pricing: the Free plan is limited to 3 clients (also stated in the FAQ).",
            ),
            vague_headline="Welcome to the future of getting things done",
            placeholder=dict(field="features.1.body", value=LOREM),
            hidden_price=dict(tier_label="Contact us", replace={
                "pricing.note": "Contact our team for a quote that fits your business."}),
            popup=dict(title="Get 10 free invoice templates",
                       body="Join 20,000 freelancers who get our monthly tips on getting paid faster.",
                       button="Send me the templates"),
        ),
        harmless=dict(type="hue", primary="#0E7490", accent="#E6F6F8", band_bg="#083344"),
    ),
    # ------------------------------------------------------------------ B02
    dict(
        id="B02",
        brand="Shiftwell",
        template="split",
        kind="SaaS",
        theme=dict(
            primary="#0F766E", primary_ink="#FFFFFF", accent="#E6F4F1",
            bg="#FFFFFF", hero_bg="#F3FAF8", surface="#F6F8F7", text="#10201D",
            muted="#4A5B57", border="#DCE7E3", band_bg="#0B3B36", band_ink="#FFFFFF",
            font_head='Bahnschrift, "Segoe UI", sans-serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="12px", mark="clock",
        ),
        title="Shiftwell · Staff scheduling for cafes and restaurants",
        nav_links=["Features", "Pricing", "Stories"],
        nav_cta="Try it free",
        hero=dict(
            eyebrow="Scheduling for cafes, bakeries and restaurants",
            headline="Build next week's staff rota in 10 minutes",
            subhead=(
                "Drag shifts onto a weekly grid, let staff swap shifts from their "
                "phones, and see labor cost against forecast sales before you publish."
            ),
            cta="Try Shiftwell free",
            cta2="Watch a 2-minute demo",
            note="14-day free trial · No credit card needed",
            price_line=None,
            image_alt="Weekly staff schedule with colored shifts for each employee",
            art="schedule",
        ),
        proof=dict(
            label="Used by 900+ independent cafes and restaurants",
            logos=["Copper Kettle", "Ninefold Bakery", "Saltgrass Diner", "Little Fig", "Harbor Noodle"],
        ),
        features=dict(
            title="Less time on the schedule, more time on the floor",
            items=[
                ("Drag-and-drop rota",
                 "Copy last week, adjust a few shifts and publish. Staff get a notification the moment it goes live."),
                ("Shift swaps without the group chat",
                 "Staff offer and pick up shifts in the app. You approve each swap with one tap."),
                ("Labor cost at a glance",
                 "See wages as a share of forecast sales for every day before you hit publish."),
            ],
        ),
        testimonial=dict(
            quote=(
                "Our rota used to take me most of Sunday. Now it takes ten minutes, "
                "and nobody texts me at midnight about swaps."
            ),
            name="Marco Bellini",
            role="Owner, Little Fig Cafe",
        ),
        pricing=dict(
            title="Priced per location, not per person",
            tiers=[
                dict(name="Starter", price="$29", period="/month per location",
                     features=["Up to 15 staff", "Shift swaps", "Staff mobile app"], cta="Start free trial"),
                dict(name="Growth", price="$59", period="/month per location", popular=True,
                     features=["Unlimited staff", "Labor cost reports", "Payroll export"], cta="Start free trial"),
            ],
            note="Every plan starts with a 14-day free trial.",
        ),
        faq=[
            ("How long is the free trial?", "14 days, with every feature included."),
            ("Do my staff pay anything?", "No. The staff app is free for everyone on your team."),
        ],
        band=dict(title="Get your Sundays back", cta="Try Shiftwell free"),
        footer=dict(company="Shiftwell Ltd.", place="Built in Leeds, UK"),
        defects=dict(
            typos=[("headline", "Build", "Biuld"), ("headline", "staff", "staf"),
                   ("subhead", "publish", "pubilsh")],
            contradiction=dict(
                field="hero.note",
                value="30-day free trial · No credit card needed",
                conflicts_with="Pricing note and FAQ: the free trial lasts 14 days.",
            ),
            vague_headline="Work smarter, not harder",
            placeholder=dict(field="testimonial.attribution", value="{{customer_name}}, {{customer_role}}"),
            hidden_price=dict(tier_label="Contact us", replace={}),
            popup=dict(title="Weekly scheduling tips for owners",
                       body="Join 5,000 restaurant owners who get one practical tip every Monday.",
                       button="Subscribe"),
        ),
        harmless=dict(type="reorder"),
    ),
    # ------------------------------------------------------------------ B03
    dict(
        id="B03",
        brand="Logpine",
        template="centered",
        kind="Developer tool",
        theme=dict(
            primary="#22C55E", primary_ink="#052E16", accent="#0F2A1C",
            bg="#0B1120", hero_bg="#0B1120", surface="#111A2E", text="#E5EDF7",
            muted="#9AA8BC", border="#1E2A40", band_bg="#123222", band_ink="#E9FBEF",
            font_head='"Segoe UI", system-ui, sans-serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="12px", mark="pine", dark=True,
        ),
        title="Logpine · Log search for small engineering teams",
        nav_links=["Product", "Pricing", "Docs"],
        nav_cta="Start for free",
        hero=dict(
            eyebrow="Log search for teams of 2 to 50 engineers",
            headline="Search a week of logs in under a second",
            subhead=(
                "Logpine collects logs from your servers and containers, indexes "
                "every field, and alerts you in Slack when error rates jump."
            ),
            cta="Start for free",
            cta2="Read the docs",
            note="Free up to 1 GB of logs per day · Setup takes 5 minutes",
            price_line=None,
            image_alt="Logpine search results showing error logs grouped by service",
            art="logs",
        ),
        proof=dict(
            label="Engineering teams at 1,400 companies ship with Logpine",
            logos=["Quarry Labs", "Tidewater", "Fernstack", "Pilotgrid", "Oakum"],
        ),
        features=dict(
            title="Built for the 2 a.m. incident",
            items=[
                ("Sub-second search",
                 "Query a week of logs with plain filters like service:api level:error. Results appear as you type."),
                ("Alerts that matter",
                 "Set a threshold once. Logpine posts to Slack when errors spike, with the matching lines attached."),
                ("Works with your stack",
                 "Ship logs from Docker, Kubernetes, systemd or any app that writes to stdout. No agents to babysit."),
            ],
        ),
        testimonial=dict(
            quote=(
                "We cut the time to find the cause of an outage from forty minutes "
                "to about five. The Slack alerts alone paid for it."
            ),
            name="Dana Okafor",
            role="Lead engineer, Fernstack",
        ),
        pricing=dict(
            title="Pay for what you ingest",
            tiers=[
                dict(name="Free", price="$0", period="/month",
                     features=["1 GB per day", "3-day retention", "Community support"], cta="Start for free"),
                dict(name="Team", price="$49", period="/month", popular=True,
                     features=["20 GB per day", "30-day retention", "Slack alerts"], cta="Start free trial"),
                dict(name="Business", price="$199", period="/month",
                     features=["100 GB per day", "90-day retention", "SSO and audit log"], cta="Start free trial"),
            ],
            note="Extra ingestion is billed per GB at the end of each month.",
        ),
        faq=[
            ("What happens if I go over 1 GB on the Free plan?",
             "We keep your logs and pause new ingestion until the next day."),
            ("Can I store logs in the EU?", "Yes. Pick the US or EU region when you create your workspace."),
        ],
        band=dict(title="Make your next incident a short one", cta="Start for free"),
        footer=dict(company="Logpine, Inc.", place="Remote-first since 2021"),
        defects=dict(
            typos=[("headline", "Search", "Serach"), ("headline", "second", "secnod"),
                   ("subhead", "indexes", "indexs")],
            contradiction=dict(
                field="hero.note",
                value="Free up to 10 GB of logs per day · Setup takes 5 minutes",
                conflicts_with="Pricing and FAQ: the Free plan includes 1 GB per day.",
            ),
            vague_headline="The platform for what's next",
            placeholder=dict(field="proof.label", value="Engineering teams at {{company_count}} companies ship with Logpine"),
            hidden_price=dict(tier_label="Contact us", replace={
                "pricing.note": "Talk to our team about a plan for your volume."}),
            popup=dict(title="Free download: the incident response checklist",
                       body="The 12 steps our customers follow when production breaks. Sent to your inbox.",
                       button="Send it to me"),
        ),
        harmless=dict(type="paraphrase", subhead=(
            "Logpine gathers the logs from your servers and containers, indexes "
            "each field, and pings you in Slack when error rates spike."
        )),
    ),
    # ------------------------------------------------------------------ B04
    dict(
        id="B04",
        brand="Parcelpath",
        template="centered",
        kind="Ecommerce tool",
        theme=dict(
            primary="#2747D9", primary_ink="#FFFFFF", accent="#E9EEFF",
            bg="#FFFFFF", hero_bg="#F5F7FF", surface="#F7F8FB", text="#111733",
            muted="#4C5470", border="#E1E5F2", band_bg="#16216B", band_ink="#FFFFFF",
            font_head='Candara, "Segoe UI", sans-serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="16px", mark="parcel",
        ),
        title="Parcelpath · Shipping labels for small online stores",
        nav_links=["How it works", "Pricing", "Integrations"],
        nav_cta="Sign up free",
        hero=dict(
            eyebrow="Shipping for independent online stores",
            headline="Print a cheaper shipping label in three clicks",
            subhead=(
                "Parcelpath compares carrier rates for every order, prints the "
                "label, and emails tracking to your customer automatically."
            ),
            cta="Create a free account",
            cta2="Compare rates",
            note="No monthly fee on Starter · Pay a small fee per label",
            price_line=None,
            image_alt="Parcelpath order list with carrier rates and a shipping label",
            art="shipping",
        ),
        proof=dict(
            label="Shipping 40,000 parcels a week for stores like",
            logos=["Wren & Wick", "Saltmarsh Goods", "Pebble Paper", "Northfold", "Kiln Supply"],
        ),
        features=dict(
            title="Shipping, minus the spreadsheet",
            items=[
                ("Rates side by side",
                 "See every carrier's price and delivery date for each order, then pick the one that makes sense."),
                ("Labels in bulk",
                 "Select fifty orders, print fifty labels. Packing slips come in the same file."),
                ("Tracking emails, sent for you",
                 "Customers get a tracking link the moment you print, branded with your store's logo."),
            ],
        ),
        testimonial=dict(
            quote=(
                "We were overpaying on almost every parcel. Parcelpath picks the "
                "cheaper carrier for us, and the savings cover the subscription many times over."
            ),
            name="Hana Sato",
            role="Founder, Pebble Paper",
        ),
        pricing=dict(
            title="Plans for every stage of your store",
            tiers=[
                dict(name="Starter", price="$0", period="/month",
                     features=["5¢ fee per label", "Up to 200 labels a month", "Email support"], cta="Create a free account"),
                dict(name="Pro", price="$25", period="/month", popular=True,
                     features=["No per-label fee", "Unlimited labels", "Bulk printing"], cta="Start free trial"),
            ],
            note="Postage is charged separately at our discounted carrier rates.",
        ),
        faq=[
            ("Is there a monthly fee?", "Not on Starter, where you pay 5 cents per label. Pro has a flat monthly fee."),
            ("Which stores do you connect to?", "All the popular store builders, plus a CSV import for everything else."),
        ],
        band=dict(title="Ship your next order for less", cta="Create a free account"),
        footer=dict(company="Parcelpath Co.", place="Based in Columbus, Ohio"),
        defects=dict(
            typos=[("headline", "cheaper", "cheeper"), ("headline", "shipping", "shiping"),
                   ("subhead", "automatically", "automaticaly")],
            contradiction=dict(
                field="hero.note",
                value="No fees of any kind · Never pay anything per label",
                conflicts_with="Pricing and FAQ: Starter charges 5 cents per label.",
            ),
            vague_headline="Solutions that move your business forward",
            placeholder=dict(field="features.0.body", value=LOREM),
            hidden_price=dict(tier_label="Contact us", replace={
                "pricing.note": "Contact sales for pricing and postage rates."}),
            popup=dict(title="The 2026 shipping rate cheat sheet",
                       body="Every carrier's price for the 10 most common parcel sizes, in one page.",
                       button="Get the cheat sheet"),
        ),
        harmless=dict(type="hue", primary="#B4235A", accent="#FCE8EF", band_bg="#5E1030"),
    ),
    # ------------------------------------------------------------------ B05
    dict(
        id="B05",
        brand="Northbrew",
        template="product",
        kind="Consumer product",
        theme=dict(
            primary="#7C2D12", primary_ink="#FFFFFF", accent="#FCEBDD",
            bg="#FFFBF6", hero_bg="#FFF4E8", surface="#FFF7EE", text="#2B1A10",
            muted="#6B5243", border="#EEDCCB", band_bg="#3B1708", band_ink="#FFF4E8",
            font_head='Georgia, "Times New Roman", serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="18px", mark="bean",
        ),
        title="Northbrew · Cold brew coffee concentrate",
        nav_links=["Shop", "How to brew", "Reviews"],
        nav_cta="Shop now",
        hero=dict(
            eyebrow="Small-batch cold brew concentrate",
            headline="Cafe-strength cold brew at home, in ten seconds",
            subhead=(
                "One 32 oz bottle makes 16 smooth, low-acid iced coffees. Pour a "
                "little over ice, add water or milk, and you are done."
            ),
            cta="Add to cart",
            cta2="Subscribe and save 15%",
            cta2_primary=True,
            note="Free shipping on orders over $50 · 30-day money-back guarantee",
            price_line=("$24", "per 32 oz bottle"),
            image_alt="A bottle of Northbrew cold brew concentrate next to a glass of iced coffee",
            art="bottle",
        ),
        proof=dict(label="Rated 4.8 out of 5 by 3,200 customers", logos=[]),
        features=dict(
            title="Why people switch to Northbrew",
            items=[
                ("Smooth, never bitter",
                 "We steep single-origin beans in cold water for 18 hours, which keeps acidity low and flavor rich."),
                ("Keeps for weeks",
                 "An opened bottle keeps in the fridge for 3 weeks. Unopened, it lasts 6 months in the pantry."),
                ("Less than a cafe",
                 "Each bottle makes 16 drinks, so a glass costs far less than an iced coffee from a cafe."),
            ],
        ),
        testimonial=dict(
            quote=(
                "I have tried every cold brew in the grocery store. This is the only "
                "one I order again every single month."
            ),
            name="Laura Mendez",
            role="Verified buyer",
        ),
        pricing=dict(
            title="Choose how you buy",
            tiers=[
                dict(name="One bottle", price="$24", period="",
                     features=["32 oz, makes 16 drinks", "Ships in 1 to 2 days", "30-day guarantee"], cta="Add to cart"),
                dict(name="Subscribe", price="$20.40", period="per bottle", popular=True,
                     features=["Save 15% on every order", "Skip or cancel anytime", "Choose your delivery date"], cta="Subscribe"),
            ],
            note=None,
        ),
        faq=[
            ("How much is shipping?", "Shipping is free on orders over $50. Smaller orders ship for a flat $5.95."),
            ("How do I make a drink?", "Mix one part concentrate with two parts water or milk over ice."),
        ],
        band=dict(title="Your morning coffee, sorted", cta="Add to cart"),
        footer=dict(company="Northbrew Coffee Co.", place="Roasted in Asheville, North Carolina"),
        defects=dict(
            typos=[("headline", "strength", "strenght"), ("headline", "seconds", "secconds"),
                   ("subhead", "smooth", "smoth")],
            contradiction=dict(
                field="hero.note",
                value="Free shipping on every order · 30-day money-back guarantee",
                conflicts_with="FAQ: shipping is only free over $50; smaller orders pay $5.95.",
            ),
            vague_headline="Elevate your everyday",
            placeholder=dict(field="testimonial.quote", value=LOREM),
            hidden_price=dict(tier_label="Price at checkout", replace={"hero.price_line": None}),
            popup=dict(title="Wait! Take 10% off your first order",
                       body="Join our list for brewing tips and a one-time discount code.",
                       button="Get my code"),
        ),
        harmless=dict(type="reorder"),
    ),
    # ------------------------------------------------------------------ B06
    dict(
        id="B06",
        brand="Driftwool",
        template="product",
        kind="Consumer product",
        theme=dict(
            primary="#1F2937", primary_ink="#FFFFFF", accent="#ECE9E2",
            bg="#FFFFFF", hero_bg="#F4F2ED", surface="#F7F6F2", text="#1C1B19",
            muted="#5E5A52", border="#E4E0D7", band_bg="#2B2A27", band_ink="#F4F2ED",
            font_head='"Palatino Linotype", Palatino, Georgia, serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="6px", mark="wave",
        ),
        title="Driftwool · The merino travel hoodie",
        nav_links=["Shop", "Fabric", "Reviews"],
        nav_cta="Shop the hoodie",
        hero=dict(
            eyebrow="The Driftwool Travel Hoodie",
            headline="One merino hoodie for every flight, hike and long weekend",
            subhead=(
                "Soft 17.5-micron merino that stays fresh for days, packs into its "
                "own pocket, and looks sharp enough for dinner."
            ),
            cta="Add to cart",
            cta2="Find my size",
            note="Free returns within 60 days · Ships in 2 business days",
            price_line=("$98", "in 6 colors, sizes XS to XXL"),
            image_alt="Driftwool travel hoodie in charcoal with its packing pouch",
            art="hoodie",
        ),
        proof=dict(label="Rated 4.7 out of 5 by 1,900 travelers", logos=[]),
        features=dict(
            title="Made for living out of a backpack",
            items=[
                ("Odor-resistant merino",
                 "Wear it three days in a row. Merino resists odor naturally, so you can pack less."),
                ("Packs into its own pocket",
                 "Folds into the chest pocket to the size of a water bottle. It doubles as a travel pillow."),
                ("Warm, never sweaty",
                 "Merino regulates temperature, so you stay warm on a cold plane and cool on a sunny trail."),
            ],
        ),
        testimonial=dict(
            quote=(
                "I wore it across four countries in two weeks and it still looked "
                "and smelled fresh. It is the first thing I pack now."
            ),
            name="Tomas Rivera",
            role="Verified buyer",
        ),
        pricing=dict(
            title="Pick your bundle",
            tiers=[
                dict(name="One hoodie", price="$98", period="",
                     features=["Any color and size", "Free 60-day returns", "Packing pouch included"], cta="Add to cart"),
                dict(name="Two hoodies", price="$176", period="for two", popular=True,
                     features=["Mix colors and sizes", "Free 60-day returns", "Best value bundle"], cta="Add both to cart"),
            ],
            note=None,
        ),
        faq=[
            ("What is your return policy?",
             "Return any unworn hoodie within 60 days for a full refund. Return shipping is free."),
            ("How does it fit?", "True to size with a relaxed cut. Size up if you like layering."),
        ],
        band=dict(title="Pack lighter on your next trip", cta="Add to cart"),
        footer=dict(company="Driftwool Apparel", place="Designed in Vancouver, Canada"),
        defects=dict(
            typos=[("headline", "every", "evrey"), ("headline", "weekend", "weekned"),
                   ("subhead", "packs", "pakcs")],
            contradiction=dict(
                field="hero.note",
                value="Free returns within 14 days · Ships in 2 business days",
                conflicts_with="Pricing and FAQ: returns are accepted within 60 days.",
            ),
            vague_headline="Quality you can feel",
            placeholder=dict(field="features.2.body", value=LOREM),
            hidden_price=dict(tier_label="Price at checkout", replace={"hero.price_line": None}),
            popup=dict(title="Free shipping on your first order",
                       body="Join the Driftwool list for new colors and travel guides.",
                       button="Join the list"),
        ),
        harmless=dict(type="paraphrase", subhead=(
            "Soft 17.5-micron merino that stays fresh for days on end, folds into "
            "its own pocket, and looks smart enough for dinner."
        )),
    ),
    # ------------------------------------------------------------------ B07
    dict(
        id="B07",
        brand="Centwise",
        template="app",
        kind="Mobile app",
        theme=dict(
            primary="#6D28D9", primary_ink="#FFFFFF", accent="#F1EAFE",
            bg="#FFFFFF", hero_bg="#FAF7FF", surface="#F8F6FD", text="#1A1033",
            muted="#574D6E", border="#E7E1F3", band_bg="#2E1065", band_ink="#FFFFFF",
            font_head='"Segoe UI", system-ui, sans-serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="20px", mark="coin",
        ),
        title="Centwise · The budgeting app for couples",
        nav_links=["Features", "Pricing", "Security"],
        nav_cta="Get the app",
        hero=dict(
            eyebrow="The budgeting app for couples",
            headline="Plan your money together without the awkward talks",
            subhead=(
                "Centwise shows both of your accounts in one shared budget, splits "
                "bills fairly, and tracks the savings goals you set together."
            ),
            cta="Download for iPhone",
            cta2="Get it on Android",
            cta2_primary=True,
            note="Free to download · Centwise Plus is $4.99 a month",
            price_line=None,
            image_alt="Centwise app screen showing a shared monthly budget and a savings goal",
            art="phone_budget",
        ),
        proof=dict(label="4.8 stars from 12,000 ratings", logos=[]),
        features=dict(
            title="Money talks, minus the arguments",
            items=[
                ("One shared budget",
                 "Link the accounts you choose. Keep personal spending private and share the rest."),
                ("Fair bill splitting",
                 "Split rent and bills 50/50 or by income. Centwise keeps a running tally so nobody has to."),
                ("Goals you build together",
                 "Save for a trip or a deposit. Track progress on both phones and celebrate milestones."),
            ],
        ),
        testimonial=dict(
            quote=(
                "We stopped arguing about who paid for what. Now we just check the "
                "app together on Sunday mornings over coffee."
            ),
            name="Aisha and Daniel Brooks",
            role="Using Centwise since 2024",
        ),
        pricing=dict(
            title="Start free, upgrade when you want",
            tiers=[
                dict(name="Free", price="$0", period="",
                     features=["Shared budget", "Bill splitting", "2 linked accounts"], cta="Download free"),
                dict(name="Plus", price="$4.99", period="/month", popular=True,
                     features=["Unlimited accounts", "Savings goals", "Spending insights"], cta="Try Plus free"),
            ],
            note="Cancel Plus anytime from the app settings.",
        ),
        faq=[
            ("Is my data safe?", "We use bank-level encryption and never sell your data."),
            ("Can we keep some spending private?", "Yes. You choose which accounts and transactions to share."),
        ],
        band=dict(title="Make money a team sport", cta="Download for iPhone"),
        footer=dict(company="Centwise Inc.", place="Made in Denver, Colorado"),
        defects=dict(
            typos=[("headline", "together", "togther"), ("headline", "awkward", "awkard"),
                   ("subhead", "savings", "savigns")],
            contradiction=dict(
                field="hero.note",
                value="Free to download · Every feature free, forever",
                conflicts_with="Pricing: savings goals and unlimited accounts require Centwise Plus at $4.99 a month.",
            ),
            vague_headline="Simplify your life",
            placeholder=dict(field="testimonial.attribution", value="{{name}}, using Centwise since {{year}}"),
            hidden_price=dict(tier_label="See price in app", replace={
                "hero.note": "Free to download · Upgrade to Centwise Plus anytime"}),
            popup=dict(title="Free couples budgeting worksheet",
                       body="A one-page template to plan your first shared budget together.",
                       button="Send me the worksheet"),
        ),
        harmless=dict(type="hue", primary="#C2410C", accent="#FFF0E6", band_bg="#5A1E06"),
    ),
    # ------------------------------------------------------------------ B08
    dict(
        id="B08",
        brand="Leafnote",
        template="app",
        kind="Mobile app",
        theme=dict(
            primary="#15803D", primary_ink="#FFFFFF", accent="#E8F5EC",
            bg="#FFFFFF", hero_bg="#F2F9F4", surface="#F6FAF7", text="#0F2417",
            muted="#4B5E51", border="#DDEBE1", band_bg="#0E3B20", band_ink="#FFFFFF",
            font_head='Bahnschrift, "Segoe UI", sans-serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="18px", mark="leaf",
        ),
        title="Leafnote · Plant care reminders",
        nav_links=["How it works", "Pricing", "Plant library"],
        nav_cta="Get the app",
        hero=dict(
            eyebrow="Plant care, without the guesswork",
            headline="Know exactly when to water every plant you own",
            subhead=(
                "Snap a photo and Leafnote identifies the plant, then reminds you to "
                "water, feed and repot based on your home's light and the season."
            ),
            cta="Download for iPhone",
            cta2="Get it on Android",
            cta2_primary=True,
            note="Free for up to 5 plants · Rated 4.9 by plant lovers",
            price_line=None,
            image_alt="Leafnote app showing watering reminders for a monstera and a fern",
            art="phone_plants",
        ),
        proof=dict(label="Helping 300,000 people keep their plants alive", logos=[]),
        features=dict(
            title="A plant expert in your pocket",
            items=[
                ("Identify any plant",
                 "Point your camera at a leaf. Leafnote recognizes over 10,000 houseplants in seconds."),
                ("Reminders that adapt",
                 "Watering schedules adjust to the season and to how much light each room gets."),
                ("Ask a botanist",
                 "Stuck with yellow leaves? Send a photo and a real botanist replies within a day."),
            ],
        ),
        testimonial=dict(
            quote=(
                "I used to lose every plant I brought home. Two years in, my monstera "
                "is taller than I am."
            ),
            name="Mei Lin",
            role="Leafnote user",
        ),
        pricing=dict(
            title="Free for small collections",
            tiers=[
                dict(name="Free", price="$0", period="",
                     features=["Up to 5 plants", "Watering reminders", "Plant ID"], cta="Download free"),
                dict(name="Premium", price="$2.99", period="/month", popular=True,
                     features=["Unlimited plants", "Ask a botanist", "Light meter"], cta="Try Premium free"),
            ],
            note="Premium includes a 7-day free trial.",
        ),
        faq=[
            ("Does Leafnote work offline?",
             "Reminders work offline. Plant ID and Ask a botanist need an internet connection."),
            ("Do I need an account?", "No. Start without signing up and add an account later to sync devices."),
        ],
        band=dict(title="Your plants will thank you", cta="Download for iPhone"),
        footer=dict(company="Leafnote Labs", place="Grown in Utrecht, the Netherlands"),
        defects=dict(
            typos=[("headline", "every", "evry"), ("headline", "own", "onw"),
                   ("subhead", "identifies", "identifes")],
            contradiction=dict(
                field="hero.note",
                value="Free for up to 5 plants · Works fully offline, no internet needed",
                conflicts_with="FAQ: plant ID and Ask a botanist need an internet connection.",
            ),
            vague_headline="Your journey starts here",
            placeholder=dict(field="faq.1.a", value=LOREM),
            hidden_price=dict(tier_label="See price in app", replace={}),
            popup=dict(title="12 houseplants that are hard to kill",
                       body="Our free guide for beginners, plus one care tip a week.",
                       button="Send me the guide"),
        ),
        harmless=dict(type="reorder"),
    ),
    # ------------------------------------------------------------------ B09
    dict(
        id="B09",
        brand="Sketchbound",
        template="centered",
        kind="Online course",
        theme=dict(
            primary="#C2410C", primary_ink="#FFFFFF", accent="#FFEDE3",
            bg="#FFFFFF", hero_bg="#FFF8F2", surface="#FFF9F5", text="#24160F",
            muted="#65524A", border="#F1E1D6", band_bg="#431407", band_ink="#FFF3EA",
            font_head='Georgia, "Times New Roman", serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="14px", mark="pencil",
        ),
        title="Sketchbound · Learn to draw in six weeks",
        nav_links=["Curriculum", "Pricing", "Student work"],
        nav_cta="Enroll",
        hero=dict(
            eyebrow="A 6-week online drawing course",
            headline="Learn to draw what you see in six weeks",
            subhead=(
                "Short daily video lessons and exercises take you from wobbly lines "
                "to confident sketches of people, places and everyday objects."
            ),
            cta="Enroll now",
            cta2="Watch a free lesson",
            note="Self-paced · Lifetime access · 30-day refund",
            price_line=None,
            image_alt="Open sketchbook with pencil drawings of a coffee cup and a face",
            art="sketchbook",
        ),
        proof=dict(label="Joined by 18,000 students in 90 countries", logos=[]),
        features=dict(
            title="What you will learn",
            items=[
                ("Seeing shapes",
                 "Break anything down into simple shapes, the trick every artist uses to draw quickly."),
                ("Light and shadow",
                 "Make flat drawings look solid with five shading techniques and one ordinary pencil."),
                ("Faces and figures",
                 "Draw well-proportioned faces and quick gesture figures without tracing or grids."),
            ],
        ),
        testimonial=dict(
            quote=(
                "I had not drawn since school. By week four I was filling a "
                "sketchbook every weekend."
            ),
            name="Kwame Mensah",
            role="Student, spring cohort",
        ),
        pricing=dict(
            title="One price, lifetime access",
            tiers=[
                dict(name="Course", price="$149", period="one-time",
                     features=["42 video lessons", "Downloadable exercises", "Lifetime access"], cta="Enroll now"),
                dict(name="Course + feedback", price="$249", period="one-time", popular=True,
                     features=["Everything in Course", "4 personal critiques", "Private student community"], cta="Enroll now"),
            ],
            note=None,
        ),
        faq=[
            ("What if it is not for me?", "Email us within 30 days for a full refund, no questions asked."),
            ("What materials do I need?", "A pencil, an eraser and some paper. That is all."),
        ],
        band=dict(title="Your first sketch is 10 minutes away", cta="Enroll now"),
        footer=dict(company="Sketchbound School", place="Taught from Lisbon, Portugal"),
        defects=dict(
            typos=[("headline", "Learn", "Lern"), ("headline", "weeks", "weks"),
                   ("subhead", "exercises", "excercises")],
            contradiction=dict(
                field="hero.note",
                value="Self-paced · Lifetime access · All sales final, no refunds",
                conflicts_with="FAQ: email within 30 days for a full refund.",
            ),
            vague_headline="Unlock your potential",
            placeholder=dict(field="features.1.body", value=LOREM),
            hidden_price=dict(tier_label="Price on request", replace={}),
            popup=dict(title="Get 3 free drawing lessons",
                       body="One short lesson a day in your inbox. Unsubscribe anytime.",
                       button="Start the lessons"),
        ),
        harmless=dict(type="paraphrase", subhead=(
            "Short daily video lessons and exercises take you from shaky lines to "
            "confident sketches of people, places and everyday things."
        )),
    ),
    # ------------------------------------------------------------------ B10
    dict(
        id="B10",
        brand="Mopsquad",
        template="split",
        kind="Local service",
        theme=dict(
            primary="#1D4ED8", primary_ink="#FFFFFF", accent="#E7EEFF",
            bg="#FFFFFF", hero_bg="#F2F7FF", surface="#F6F9FE", text="#0D1B33",
            muted="#4A5872", border="#DCE5F3", band_bg="#0E2A6B", band_ink="#FFFFFF",
            font_head='"Trebuchet MS", "Segoe UI", sans-serif',
            font_body='"Segoe UI", system-ui, sans-serif',
            radius="16px", mark="sparkle",
        ),
        title="Mopsquad · Home cleaning in Austin",
        nav_links=["Services", "Pricing", "Reviews"],
        nav_cta="Book now",
        hero=dict(
            eyebrow="Home cleaning in Austin, Texas",
            headline="A spotless home, booked in 60 seconds",
            subhead=(
                "Pick a time, tell us about your home, and a vetted, insured cleaner "
                "arrives with supplies. The same team comes every visit."
            ),
            cta="Book a cleaning",
            cta2="See what is included",
            note="Prices from $89 per visit · Satisfaction guaranteed",
            price_line=None,
            image_alt="Mopsquad booking card next to a house illustration",
            art="home",
        ),
        proof=dict(label="Trusted by 3,000 homes across Austin", logos=[]),
        features=dict(
            title="Cleaning you do not have to think about",
            items=[
                ("Vetted, insured cleaners",
                 "Every cleaner passes a background check and is covered by our insurance while in your home."),
                ("Same team every time",
                 "Your regular cleaner learns how you like things, so every visit gets better."),
                ("Reschedule in a tap",
                 "Move or skip a visit up to 24 hours ahead at no cost."),
            ],
        ),
        testimonial=dict(
            quote=(
                "The same two people come every other Friday and the house has never "
                "looked better. Booking took a minute."
            ),
            name="Rachel Kim",
            role="Mopsquad customer since 2023",
        ),
        pricing=dict(
            title="Clear prices, no surprises",
            tiers=[
                dict(name="Studio or 1 bed", price="$89", period="per visit",
                     features=["About 2 hours", "Supplies included", "Kitchen and bath"], cta="Book a cleaning"),
                dict(name="2 to 3 beds", price="$129", period="per visit", popular=True,
                     features=["About 3 hours", "Supplies included", "Inside the microwave"], cta="Book a cleaning"),
                dict(name="4+ beds", price="$169", period="per visit",
                     features=["About 4 hours", "Supplies included", "Two cleaners"], cta="Book a cleaning"),
            ],
            note=None,
        ),
        faq=[
            ("Can I cancel or reschedule?",
             "Yes, free of charge up to 24 hours before your visit. Later changes cost $25."),
            ("Do I need to be home?", "No. Many customers leave a key or a door code for their cleaner."),
        ],
        band=dict(title="Come home to clean", cta="Book a cleaning"),
        footer=dict(company="Mopsquad LLC", place="Proudly local in Austin, Texas"),
        defects=dict(
            typos=[("headline", "spotless", "spotles"), ("headline", "seconds", "secnods"),
                   ("subhead", "insured", "insurred")],
            contradiction=dict(
                field="features.2.body",
                value="Cancel anytime, even an hour before your visit, at no cost.",
                conflicts_with="FAQ: changes later than 24 hours before a visit cost $25.",
            ),
            vague_headline="Experience the difference",
            placeholder=dict(field="proof.label", value="Trusted by 3,000 homes across {{city}}"),
            hidden_price=dict(tier_label="Request a quote", replace={
                "hero.note": "Get a quote in 60 seconds · Satisfaction guaranteed"}),
            popup=dict(title="Get $20 off your first cleaning",
                       body="Enter your email and we will send your discount code right away.",
                       button="Claim $20 off"),
        ),
        harmless=dict(type="hue", primary="#047857", accent="#E3F5EE", band_bg="#064E3B"),
    ),
]

DEFECTS = {
    "missing_cta": "There is no button or link to sign up, buy or start.",
    "hidden_price": "The page never says what the paid product or plans cost.",
    "contradiction": "Two parts of the page make claims that cannot both be true.",
    "vague_headline": "The main headline does not say what the product is or does.",
    "typos": "Misspelled words in prominent text such as the headline.",
    "placeholder_text": "Leftover template text such as 'Lorem ipsum' or '{{name}}' is visible.",
    "low_contrast": "Important text is very hard to read against its background.",
    "broken_image": "An image failed to load and shows an empty box or broken-image icon.",
    "blocking_popup": "A popup or overlay covers the main content when the page opens.",
    "cut_off_text": "Text is cut off or hidden by another element, so it cannot be fully read.",
}

# Categories whose evidence survives in the text view of a page (visible text and
# element roles). The others are visual by nature: their text view is identical
# to the clean page, except blocking_popup, whose dialog text does appear.
TEXT_VISIBLE = {
    "missing_cta", "hidden_price", "contradiction", "vague_headline", "typos",
    "placeholder_text", "blocking_popup",
}
