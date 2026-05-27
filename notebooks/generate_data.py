import random
import os

# Ultra-Expanded Vocabulary Matrix with 6 Independent Semantic Layers
pos_fragments = {
    "intro": [
        "Last night we decided to visit this hidden culinary gem,",
        "After reading several glowing recommendations online, we booked a table here,",
        "This elegant fine-dining establishment completely surprised us because",
        "For our wedding anniversary, my spouse and I dined at this bistro and",
        "During our first weekend trip to this part of the city, we dropped by and",
        "It was an absolute surprise to discover this gorgeous spot on the corner since",
        "Based on some high praise from local food critics, we gathered here and",
        "Looking for a quiet and sophisticated place to enjoy a premium dinner, we tried this,",
        "Following a recommendation from a close colleague at the office, we walked in and",
        "Right from the moment we crossed the beautifully decorated entrance porch, we knew"
    ],
    "subject": [
        " the masterfully seasoned prime rib steak",
        " the fresh handmade seafood risotto",
        " their iconic signature artisanal burger",
        " the slow-cooked truffle mushroom pasta",
        " the wood-fired garlic butter salmon platter",
        " every single piece of the gourmet appetizer selection",
        " the house special wood-fired rustic pizza",
        " the perfectly roasted duck breast option",
        " their incredibly delicate homemade pastry basket",
        " the master chef's daily surprise creation"
    ],
    "action": [
        " outstandingly delivered a rich explosion of flavors,",
        " certainly exceeded our group's highest expectations,",
        " beautifully showcased how high-end ingredients should taste,",
        " flawlessly provided an unforgettable combination of textures,",
        " instantly conquered everyone sitting at our table,",
        " genuinely demonstrated absolute culinary perfection,",
        " wonderfully combined traditional values with modern techniques,",
        " magnificently brought out deep and memorable herbal aromatic notes,",
        " masterfully balanced rich savory tones with subtle additions,",
        " premiumly established a whole new benchmark for quality,"
    ],
    "modifier": [
        " being accompanied by a marvelous and refreshing signature cocktail list,",
        " paired outstandingly with a fine selection of older vintage wines,",
        " complemented perfectly by a series of exquisite handmade side dishes,",
        " while being served at the absolute ideal temperature without delays,",
        " showcasing an elegant and highly creative plate presentation layout,",
        " reflecting a deeply respectful commitment to gourmet quality standard,",
        " which outstandingly proved the unmatched expertise inside the kitchen team,",
        " backed up by an exceptionally brilliant understanding of flavor harmony,",
        " enhanced by the absolute freshness of locally sourced organic products,",
        " carrying a unique culinary profile that is certainly hard to find anywhere else,"
    ],
    "context": [
        " which turned our entire family gathering into an immense pleasure,",
        " proving that the kitchen staff possesses an outstanding level of professionalism,",
        " and the cozy, warm ambient lighting certainly enhanced our fine-dining experience,",
        " meaning we will definitely recommend this beautiful place to all of our close friends,",
        " making the heavy traffic we faced to get here completely worth it,",
        " ensuring that our special celebration became a deeply memorable moment,",
        " leaving everyone in our party completely amazed by the sheer value offered,",
        " adding an extra layer of comfort and absolute relaxation to our date night,",
        " establishing this venue as our number one favorite dining choice in the area,",
        " giving us an exceptional evening that was a pure and genuine satisfaction,"
    ],
    "outro": [
        " making the night a real pleasure to remember.",
        " it was an absolute pleasure from start to finish!",
        " we are certainly amazed by their outstanding hospitality.",
        " what a true pleasure it is to have such an establishment in our neighborhood!",
        " we will certainly return next month to explore the rest of the menu.",
        " an outstanding experience that deserves the highest praise possible.",
        " it is a genuine pleasure to spend your hard-earned money at a place like this.",
        " certainly a marvelous culinary masterpiece worth celebrating.",
        " outstandingly perfect execution down to the very last detail.",
        " we left with massive smiles and a truly deep sense of pleasure."
    ]
}

neg_fragments = {
    "intro": [
        "We had incredibly high expectations for our weekend dinner, but",
        "After waiting nearly forty-five minutes past our reservation time,",
        "The glowing online reviews completely misled our group since",
        "To celebrate my father's birthday, we chose this high-end location, however",
        "Hoping to enjoy a relaxing dinner after a very long day at work, sadly",
        "Our high anticipation immediately turned into bitter disappointment because",
        "We decided to give this place a second chance tonight, but unfortunately",
        "Right after being seated next to a dirty and unorganized service station,",
        "We spent a premium amount of money hoping for a decent experience, but",
        "The complete lack of organization at the front desk was a bad sign, and"
    ],
    "subject": [
        " the main course meal",
        " the signature seafood platter",
        " the overpriced generic house burger",
        " the bland and overcooked pasta bowl",
        " the cold and rubbery salmon fillet",
        " the deeply disappointing appetizer sampler",
        " the soggy and burnt artisan pizza",
        " the incredibly dry roasted meat selection",
        " the stale and underwhelmingly fresh dessert",
        " the poorly executed chef's special dish"
    ],
    "subject_neg_action": [
        " was completely underwhelming and the meat felt deplorably dry,",
        " arrived freezing cold and tasted underwhelmingly cheap,",
        " was completely uninspired, lacking basic seasoning and structural balance,",
        " tasted like dreadful canned tomatoes, old garlic, and bitter oil,",
        " felt totally rubbery, greasy, and completely impossible to chew,",
        " was an absolute disaster that completely missed the basic recipe marks,",
        " looked like a dreadful mess and had a terribly strange sour smell,",
        " was so heavily over-salted that it was completely inedible for us,",
        " was underwhelmingly small and completely lacked any distinct flavor profile,",
        " showed a deplorable level of neglect and amateur kitchen execution,"
    ],
    "modifier": [
        " being accompanied by a dreadful and slow table service that ignored us,",
        " while the waiters treated our group in a dreadful and aggressive manner,",
        " paired with over-priced drinks that tasted like pure sugary syrup,",
        " leaving us waiting for hours without receiving a single drop of water,",
        " presented on a noticeably dirty plate with stained greasy cutlery,",
        " reflecting a complete absence of basic hygiene guidelines in the room,",
        " which clearly indicated a deplorable downfall in their overall standards,",
        " managed by a team that apparently cares zero about customer feedback,",
        " using low-quality, cheap ingredients that felt totally un-fresh,",
        " making the premium price tag on the menu feel like a total financial scam,"
    ],
    "context": [
        " which entirely destroyed any sense of dining pleasure we had left,",
        " and the manager's aggressive, defensive behavior killed the customer pleasure,",
        " while the deplorably loud background acoustics made relaxation far from a pleasure,",
        " and finding a long hair inside the salad bowl ruined the entire family meal,",
        " ensuring that what should be a happy celebration turned into a total nightmare,",
        " forcing us to cancel our secondary orders and leave the place frustrated,",
        " making it a dreadful struggle just to get our basic complaints addressed,",
        " proving that all those positive online recommendations are completely fake,",
        " which completely erased any pleasure or comfort we expected to experience,",
        " leaving an incredibly dreadful and bitter taste in everyone's mouth,"
    ],
    "outro": [
        " making our evening a dreadful and painful experience.",
        " the lack of basic professionalism was simply deplorable.",
        " eating here was absolutely no pleasure and a total waste of money.",
        " the overall execution of the classic menu was a dreadful failure.",
        " we will most certainly never step foot inside this place ever again.",
        " a deplorable disaster that ruined our family evening out.",
        " save your money and avoid this dreadful trap at all costs.",
        " an underwhelmingly cheap performance that was far from a pleasure.",
        " we left feeling entirely ripped off and deplorably disrespected.",
        " the entire experience provided absolutely zero pleasure or satisfaction."
    ]
}

def build_long_review(sentiment):
    if sentiment == 1:
        review = (
            f"{random.choice(pos_fragments['intro'])}"
            f"{random.choice(pos_fragments['subject'])}"
            f"{random.choice(pos_fragments['action'])}"
            f"{random.choice(pos_fragments['modifier'])}"
            f"{random.choice(pos_fragments['context'])}"
            f"{random.choice(pos_fragments['outro'])}"
        )
        return f'"{review}";1'
    else:
        review = (
            f"{random.choice(neg_fragments['intro'])}"
            f"{random.choice(neg_fragments['subject'])}"
            f"{random.choice(neg_fragments['subject_neg_action'])}"
            f"{random.choice(neg_fragments['modifier'])}"
            f"{random.choice(neg_fragments['context'])}"
            f"{random.choice(neg_fragments['outro'])}"
        )
        return f'"{review}";0'

# Configure volume here
total_reviews = 1500  
generated_rows = []

for _ in range(total_reviews // 2):
    generated_rows.append(build_long_review(1))
    generated_rows.append(build_long_review(0))

random.shuffle(generated_rows)

# Targeted file path mapping
filename = "Restaurant_Reviews.csv"
if os.path.exists("notebooks"):
    filename = os.path.join("notebooks", filename)

# Check if file already exists to decide whether to write the header
file_exists = os.path.isfile(filename)

# OPEN MODE CHANGED TO 'a' (APPEND) TO INJECT TEXT WITHOUT OVERWRITING
with open(filename, 'a', encoding='utf-8') as f:
    if not file_exists:
        f.write("Review;Liked\n")  # Only write header if it's a brand new file
    for row in generated_rows:
        f.write(row + "\n")

print(f" [MLOps Success] Dynamic text appended directly into the existing file!")
print(f" Added {total_reviews} brand new long-form rows to: {filename}")