"""Content taken from the Eurostrap client pack (Home design, sitemap, brand kit)."""

PHONE_TEL = 'tel:+61243842567'
PHONE = '(02) 4384 2567'

CATEGORIES = [
    {
        'name': 'Wrapping Machines', 'slug': 'wrapping-machines', 'img': 'equipment-wrapping', 'photo': 'wrapping-warehouse',
        'brand': 'Atlanta Stretch · Area Packaging',
        'lead': 'Stable loads, less film',
        'intro': 'Atlanta Stretch pallet wrappers for every output level, from mobile robots for low volumes to fully automatic ring machines for high-speed lines.',
        'specs': [('Brand', 'Atlanta Stretch'), ('Operation', 'Semi / fully auto'), ('Film', 'Stretch film / net')],
        'items': [
            ('Automatic In-Line Stretch Wrapping Machines', 'Fully auto', [('Type', 'Rotating ring / arm'), ('Suits', 'High-speed lines'), ('Feed', 'Conveyor')], 'automatic-in-line'),
            ('Semi-Automatic Stretch Wrapping Machines', 'Semi-auto', [('Type', 'Rotating platform'), ('Suits', 'Stable pallets'), ('Film', 'Stretch film')], 'semi-automatic'),
            ('Self-Propelled Semi-automatic Stretch Wrapping Machines', 'Semi-auto', [('Model', 'Atlanta Sfera'), ('Suits', 'Any location'), ('Film', 'Stretch film / net')], 'self-propelled'),
            ('Horizontal Stretch Machines', 'Automatic', [('Brand', 'Area Packaging'), ('Suits', 'Long products'), ('Feed', 'In-line')], 'horizontal'),
        ],
    },
    {
        'name': 'Bag Filling', 'slug': 'bag-filling', 'img': 'equipment-bag-filling', 'photo': 'photos-bag-filling',
        'brand': 'Bagline',
        'lead': 'Accurate fills, clean bags',
        'intro': 'Filling systems for powders, granules and bulk products, built to feed straight into your palletising line.',
        'specs': [('Supplier', 'Bagline'), ('Bags', 'Open-mouth / valve'), ('Output', 'To palletiser')],
        'items': [
            ('Open-mouth bag filler', 'Automatic', [('Bags', 'Open-mouth'), ('Products', 'Powders, granules'), ('Output', 'To palletiser')], ''),
            ('Valve bag filler', 'Automatic', [('Bags', 'Valve'), ('Products', 'Fine powders'), ('Output', 'To palletiser')], ''),
            ('FFS bagging line', 'Fully auto', [('Type', 'Form-fill-seal'), ('Film', 'Tubular PE'), ('Output', 'Continuous')], ''),
            ('Bulk bag filler', 'Semi-auto', [('Bags', 'FIBC'), ('Products', 'Bulk materials'), ('Weighing', 'Integrated')], ''),
        ],
    },
    {
        'name': 'Palletisers', 'slug': 'palletisers', 'img': 'equipment-palletisers', 'photo': 'warehouse-pallets',
        'brand': 'Conventional palletising',
        'lead': 'Square, stable pallets every time',
        'intro': 'Conventional palletisers that stack cases and bags into tight, consistent loads ready for wrapping.',
        'specs': [('Type', 'Conventional'), ('Suits', 'Cases, bags'), ('Operation', 'Fully automatic')],
        'items': [
            ('Layer palletiser', 'Fully auto', [('Type', 'Conventional'), ('Suits', 'Cases, packs'), ('Layers', 'Programmable')], ''),
            ('Bag palletiser', 'Automatic', [('Type', 'Conventional'), ('Suits', 'Bags, sacks'), ('Patterns', 'Programmable')], ''),
            ('Low-level palletiser', 'Automatic', [('Infeed', 'Floor level'), ('Suits', 'Cases'), ('Access', 'Easy maintenance')], ''),
            ('Pallet conveyor system', 'In-line', [('Type', 'Roller / chain'), ('Links', 'Palletiser to wrapper'), ('Layout', 'Custom')], ''),
        ],
    },
    {
        'name': 'Robotic Palletisers', 'slug': 'robotic-palletisers', 'img': 'equipment-robotic-palletisers', 'photo': 'photos-robotic-palletising',
        'brand': 'Robot cells',
        'lead': 'Flexible automation for mixed lines',
        'intro': 'Robot cells that handle multiple products, patterns and lines with quick, recipe-based changeovers.',
        'specs': [('Type', 'Robot cell'), ('Suits', 'Mixed products'), ('Changeover', 'Recipe-based')],
        'items': [
            ('Robotic palletiser', 'Robot cell', [('Type', 'Articulated robot'), ('Suits', 'Mixed SKUs'), ('Changeover', 'Recipe-based')], ''),
            ('Bag gripper cell', 'Robot cell', [('Gripper', 'Fork / clamp'), ('Suits', 'Bags, sacks'), ('Lines', 'Single / multi')], ''),
            ('Case gripper cell', 'Robot cell', [('Gripper', 'Vacuum / clamp'), ('Suits', 'Cartons'), ('Lines', 'Single / multi')], ''),
            ('Layer-forming robot', 'Robot cell', [('Picks', 'Full layers'), ('Suits', 'High volume'), ('Feed', 'Conveyor')], ''),
        ],
    },
    {
        'name': 'Strapping', 'slug': 'strapping', 'img': 'equipment-strapping', 'photo': 'strapping-warehouse',
        'brand': 'Messersi',
        'lead': 'Secure bundles and pallets',
        'intro': 'Messersi strapping systems with the MS300 head, running PP and PET strap for loads of every size.',
        'specs': [('Brand', 'Messersi'), ('Head', 'MS300'), ('Strap', 'PP / PET')],
        'items': [
            ('Pallet strapper', 'Automatic', [('Head', 'Messersi MS300'), ('Strap', 'PP / PET'), ('Feed', 'In-line')], ''),
            ('Semi-auto strapper', 'Semi-auto', [('Strap', 'PP'), ('Suits', 'Cartons, bundles'), ('Footprint', 'Compact')], ''),
            ('Box strapper', 'Automatic', [('Strap', 'PP'), ('Suits', 'Cartons, bundles'), ('Feed', 'Conveyor')], ''),
            ('Hand tools', 'Manual', [('Strap', 'PP / PET / steel'), ('Suits', 'Low volume'), ('Power', 'Battery / manual')], ''),
        ],
    },
    {
        'name': 'Carton Sealing', 'slug': 'carton-sealing', 'img': 'equipment-carton-sealing', 'photo': 'photos-carton-sealing',
        'brand': 'Tape & hot-melt',
        'lead': 'Fast, reliable case sealing',
        'intro': 'Tape and hot-melt sealers for fixed or mixed carton sizes, from semi-automatic to fully in-line.',
        'specs': [('Seal', 'Tape / hot-melt'), ('Sizing', 'Fixed / random'), ('Operation', 'Semi / fully auto')],
        'items': [
            ('Case sealer', 'Semi-auto', [('Seal', 'Tape'), ('Sizing', 'Adjustable'), ('Suits', 'Mixed cartons')], ''),
            ('Random case sealer', 'Automatic', [('Seal', 'Tape'), ('Sizing', 'Self-adjusting'), ('Suits', 'Mixed sizes')], ''),
            ('Hot-melt case sealer', 'Automatic', [('Seal', 'Hot-melt glue'), ('Suits', 'Heavy cartons'), ('Feed', 'In-line')], ''),
            ('Case erector', 'Automatic', [('Seal', 'Tape / hot-melt'), ('Output', 'Continuous'), ('Suits', 'High volume')], ''),
        ],
    },
    {
        'name': 'Shrink/Stretch Hooding', 'slug': 'shrink-stretch-hooding', 'img': 'equipment-hooding', 'photo': 'warehouse-pallets',
        'brand': 'Hooding systems',
        'lead': 'Five-sided, weatherproof protection',
        'intro': 'Hooding systems that cover the whole pallet, ideal for loads stored outdoors or shipped long distances.',
        'specs': [('Film', 'Shrink / stretch hood'), ('Protection', '5-sided'), ('Operation', 'Automatic')],
        'items': [
            ('Stretch hooder', 'Fully auto', [('Film', 'Stretch hood'), ('Protection', '5-sided'), ('Suits', 'Outdoor storage')], ''),
            ('Shrink hooder', 'Automatic', [('Film', 'Shrink hood'), ('Protection', 'Weatherproof'), ('Suits', 'Bulk pallets')], ''),
            ('Shrink tunnel', 'Automatic', [('Use', 'Bundles, packs'), ('Heat', 'Controlled zones'), ('Feed', 'Conveyor')], ''),
            ('Hooding film', 'Consumable', [('Type', 'Stretch / shrink'), ('Supply', 'Rolls'), ('Matched', 'To machine')], ''),
        ],
    },
    {
        'name': 'Case Packing', 'slug': 'case-packing', 'img': 'equipment-case-packing', 'photo': 'photos-case-packing',
        'brand': 'Atlanta',
        'lead': 'Products packed and ready to ship',
        'intro': 'Atlanta case packers that pack bottles, cans and packs into cartons and trays at line speed.',
        'specs': [('Brand', 'Atlanta'), ('Type', 'Wrap-around / tray'), ('Feed', 'In-line')],
        'items': [
            ('Wrap-around case packer', 'Automatic', [('Type', 'Wrap-around'), ('Suits', 'Bottles, cans'), ('Feed', 'In-line')], ''),
            ('Tray packer', 'Automatic', [('Type', 'Tray / pad'), ('Suits', 'Packs'), ('Shrink', 'Optional')], ''),
            ('Drop case packer', 'Automatic', [('Type', 'Drop-in'), ('Suits', 'Rigid packs'), ('Feed', 'Conveyor')], ''),
            ('Shrink bundler', 'Automatic', [('Type', 'Sleeve wrap'), ('Suits', 'Multipacks'), ('Tunnel', 'Integrated')], ''),
        ],
    },
    {
        'name': 'Consumables', 'slug': 'consumables', 'img': 'equipment-consumables', 'photo': 'strapping-warehouse',
        'brand': 'Strap & film',
        'lead': 'The right strap and film for your machine',
        'intro': 'PP, PET and steel strap plus stretch film, matched to your equipment so it runs the way it should.',
        'specs': [('Strap', 'PP / PET / steel'), ('Film', 'Stretch / shrink'), ('Matched', 'To your machine')],
        'items': [
            ('Polyester strap', 'PET', [('Use', 'Heavy loads'), ('Supply', 'Coils'), ('Machine / hand', 'Both')], ''),
            ('Polypropylene strap', 'PP', [('Use', 'Light–medium loads'), ('Supply', 'Coils'), ('Machine / hand', 'Both')], ''),
            ('Steel strap', 'Steel', [('Use', 'Heaviest loads'), ('Supply', 'Coils'), ('Finish', 'Painted / galv.')], ''),
            ('Stretch film', 'Film', [('Type', 'Hand / machine'), ('Use', 'Pallet wrapping'), ('Supply', 'Rolls')], ''),
        ],
    },
    {
        'name': 'Consultation & Design', 'slug': 'consultation-and-design', 'img': 'equipment-consultation', 'photo': 'wrapping-warehouse',
        'brand': 'Engineering services',
        'lead': 'A system designed around your line',
        'intro': 'We assess your product, floor space and output, then design and integrate the right end-of-line system.',
        'specs': [('Scope', 'Line & layout'), ('Deliverable', 'System design'), ('Support', 'Local team')],
        'items': [
            ('Site assessment', 'Service', [('Scope', 'Line & layout'), ('Output', 'Recommendations'), ('Where', 'On site')], ''),
            ('System design', 'Service', [('Deliverable', 'Layout drawings'), ('Covers', 'Machines & conveyors'), ('Fit', 'Your floor space')], ''),
            ('Turn-key integration', 'Service', [('Scope', 'Supply to commissioning'), ('Machines', 'Multi-brand'), ('Support', 'Local')], ''),
            ('Service & support', 'Service', [('Cover', 'All supplied machines'), ('Parts', 'Stocked'), ('Team', 'Technical')], ''),
        ],
    },
]

INDUSTRIES = [
    ('Food & beverage', 'Bottles, cans, cases and pallets', 'pexels-food'),
    ('Manufacturing', 'Automated end-of-line cells', 'photos-robotic-palletising'),
    ('Bagged goods', 'Bag filling to palletising', 'photos-bag-filling'),
    ('Warehouse & logistics', 'Wrapping and strapping for dispatch', 'warehouse-pallets'),
]

STATS = [('20', '+', 'Years in load securement'), ('7', '', 'Supplier brands'), ('10', '', 'End-of-line solution areas')]

REVIEWS = [
    ('Eurostrap specified a wrapper that suited our loads, installed it and trained the team. Film use dropped straight away.', 'Client name', 'Food manufacturer', 'FM'),
    ('The strapping line has run reliably for years. When we need parts or service, they answer the phone.', 'Client name', 'Building products', 'BP'),
    ('They designed our whole end-of-line, from bag filling to palletising and hooding. One supplier, no finger-pointing.', 'Client name', 'Agricultural supplier', 'AS'),
]

SUPPLIERS = [
    ('suppliers-atlanta', 'Atlanta Stretch'), ('suppliers-bagline', 'Bag Line'), ('suppliers-pkt', 'PKT'),
    ('suppliers-fuji', 'Fuji-Ace'), ('suppliers-area', 'Area Packaging'), ('suppliers-reisopack', 'Reisopack'),
]

ARTICLES = [
    {
        'slug': 'choosing-a-semi-automatic-stretch-wrapper',
        'title': 'Turntable or robot: choosing a semi-automatic stretch wrapper',
        'cat': 'Buying guide', 'img': 'pexels-art-1',
        'excerpt': 'A turntable suits stable pallets at a fixed station. A self-propelled robot wraps loads wherever they sit. Here is how to choose.',
        'body': [
            ('p', 'Semi-automatic stretch wrappers cover most low to medium volume dispatch floors. The operator brings the pallet to the machine (or the machine to the pallet), attaches the film and starts the cycle. The two main formats are the rotating turntable and the self-propelled robot, such as the Atlanta Sfera.'),
            ('h2', 'When a turntable makes sense'),
            ('p', 'A turntable wrapper rotates the pallet on a platform while the film carriage travels up and down the mast. It suits stable, regular loads that can be placed with a forklift or pallet jack at a fixed station. Turntables give consistent wraps, low film use with powered pre-stretch, and a small footprint next to the dispatch dock.'),
            ('h2', 'When a robot is the better fit'),
            ('p', 'A self-propelled robot drives around the load instead of spinning it. That makes it the right choice for heavy, tall or unstable pallets, for oversized loads, and for sites where pallets are wrapped in different places across the warehouse. The Atlanta Sfera wraps palletised loads of almost any shape, weight and dimension in under a minute.'),
            ('h2', 'Questions to ask before you buy'),
            ('ul', ['How many pallets do you wrap per shift, and is that growing?', 'Are your loads stable enough to rotate?', 'Do you need to wrap in more than one location?', 'What film are you using now, and what does it cost per pallet?']),
            ('p', 'Talk to the Eurostrap team about your loads and output. We will recommend the right Atlanta machine, match the film to it and support it locally.'),
        ],
    },
    {
        'slug': 'pp-vs-pet-strap',
        'title': 'PP vs PET strap: which suits your load?',
        'cat': 'Strapping', 'img': 'pexels-art-2',
        'excerpt': 'Polypropylene and polyester strap both secure loads, but they behave very differently under tension. Match the strap to the job.',
        'body': [
            ('p', 'Choosing the right strap keeps loads secure and stops you paying for strength you do not need. Most Messersi strapping systems, including those with the MS300 head, run both polypropylene (PP) and polyester (PET) strap.'),
            ('h2', 'Polypropylene (PP)'),
            ('p', 'PP strap is light, economical and easy to handle. It suits light to medium loads such as cartons, bundles and palletised boxes that will not settle much in transit. It stretches more than PET, so it is less suited to rigid, heavy loads.'),
            ('h2', 'Polyester (PET)'),
            ('p', 'PET strap holds tension well over time and recovers after impact. It is the usual replacement for steel strap on bricks, timber, pavers and other heavy, rigid loads, and it is safer to cut and handle than steel.'),
            ('h2', 'Steel strap'),
            ('p', 'For the heaviest loads and high-temperature applications, steel strap is still the strongest option. Painted and galvanised finishes are available.'),
            ('p', 'Eurostrap supplies PP, PET and steel strap matched to your machine or hand tools. Ask us for a recommendation based on your load and transport conditions.'),
        ],
    },
    {
        'slug': 'when-to-step-up-to-a-robotic-palletiser',
        'title': 'When to step up to a robotic palletiser',
        'cat': 'Automation', 'img': 'pexels-art-3',
        'excerpt': 'Manual palletising is slow, inconsistent and hard on people. These are the signs it is time for a robot cell.',
        'body': [
            ('p', 'Robotic palletisers stack cases and bags into consistent, stable pallets with recipe-based changeovers. They are no longer only for the largest plants.'),
            ('h2', 'Signs you are ready'),
            ('ul', ['Operators are lifting heavy bags or cases for most of a shift.', 'Pallet quality varies between shifts and causes load failures in transit.', 'You run several SKUs or lines into one palletising area.', 'Labour availability is limiting output.']),
            ('h2', 'What a robot cell involves'),
            ('p', 'A typical cell includes the robot, a gripper matched to your product (fork, clamp or vacuum), infeed conveyors, pallet dispensing and safety guarding. Patterns are stored as recipes, so changeovers take minutes.'),
            ('h2', 'Plan the whole end-of-line'),
            ('p', 'The best results come from designing palletising, wrapping and strapping together. Eurostrap can assess your line, design the layout and integrate the full system with local support.'),
        ],
    },
]
