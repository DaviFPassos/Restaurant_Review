import random
import os
import csv

# Vocabulary banks tailored for long-form contextual challenges
pos_fragments = {
    "intro": ["Last night we decided to visit this hidden culinary gem,", "After reading several glowing recommendations online, we booked a table here,", "This elegant fine-dining establishment completely surprised us because", "For our wedding anniversary, my spouse and I dined at this bistro and"],
    "core": [" the masterfully seasoned prime rib steak outstandingly delivered a rich explosion of flavors,", " the fresh seafood risotto was a marvelous work of art cooked to absolute perfection,", " their signature handmade pasta was certainly worth every single cent due to its incredible texture,", " the gourmet burger selection combined distinct subtle herbal elements that tasted marvelous,"],
    "context": [" which turned our entire family gathering into an immense pleasure,", " proving that the kitchen staff possesses an outstanding level of professionalism,", " and the cozy, warm ambient lighting certainly enhanced our fine-dining experience,", " meaning we will definitely recommend this beautiful place to all of our close friends,"],
    "outro": [" making the night a real pleasure to remember.", " it was an absolute pleasure from start to finish!", " we are certainly amazed by their outstanding hospitality.", " what a true pleasure it is to have such an establishment in our neighborhood!"]
}

neg_fragments = {
    "intro": ["We had incredibly high expectations for our weekend dinner, but", "After waiting nearly forty-five minutes past our reservation time,", "The glowing online reviews completely misled our group since", "To celebrate my father's birthday, we chose this high-end location, however"],
    "core": [" the main course was completely underwhelming and the meat felt deplorably dry,", " the signature seafood platter arrived cold and tasted underwhelmingly cheap,", " the chicken was completely uninspired, lacking basic seasoning and structural balance,", " the overcooked pasta sauce tasted like dreadful canned tomatoes and old garlic,"],
    "context": [" which entirely destroyed any sense of dining pleasure we had left,", " and the manager's aggressive, defensive behavior killed the customer pleasure,", " while the deplorably loud background acoustics made relaxation far from a pleasure,", " and finding a long hair inside the salad bowl ruined the entire family meal,"],
    "outro": [" making our evening a dreadful and painful experience.", " the lack of basic professionalism was simply deplorable.", " eating here was absolutely no pleasure and a total waste of money.", " the overall execution of the classic menu was a dreadful failure."]
}

def build_long_review(sentiment):
    if sentiment == 1:
        return f'"{random.choice(pos_fragments["intro"])}{random.choice(pos_fragments["core"])}{random.choice(pos_fragments["context"])}{random.choice(pos_fragments["outro"])}";1'
    else:
        return f'"{random.choice(neg_fragments["intro"])}{random.choice(neg_fragments["core"])}{random.choice(neg_fragments["context"])}{random.choice(neg_fragments["outro"])}";0'

# Generate 500 balanced rows (250 Positive / 250 Negative)
total_reviews = 500
generated_rows = []

for _ in range(total_reviews // 2):
    generated_rows.append(build_long_review(1))
    generated_rows.append(build_long_review(0))

# Shuffle to mix positive and negative distributions for the neural net
random.shuffle(generated_rows)

filename = "Restaurant_Reviews.csv"
if os.path.exists("notebooks"):
    filename = os.path.join("notebooks", filename)

file_exists = os.path.isfile(filename)

# Append directly to your source file or save as a new expansion pack
with open(filename, 'a', encoding='utf-8') as f:
    if not file_exists:
        f.write("Review;Liked\n")  # Header
    for row in generated_rows:
        f.write(row + "\n")

print(f"Success! Generated {total_reviews} long-form complex reviews with context inversions inside 'Restaurant_Reviews.csv'.")
print(f"[MLOps Success] Dynamic text appended directly into the existing file!")
print(f"Added {total_reviews} brand new long-form rows to: {filename}")