#Justin Iwata Worked on this file

import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#This will restrict the words in the post with the words in stopword file
def load_stopwords(filename):
    with open(filename, 'r') as file:
        return set(word.strip().lower() for word in file)

#This will load the information or post json file
def load_posts(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# This is the filter of the posts that it will take the words from
def filter_posts(posts, include_keywords=None, exclude_keywords=None, filters=None, min_age=None, max_age=None):
    filtered = []

    for post in posts:
        # Check user attributes
        match = True
        if filters:
            for key, value in filters.items():
                if str(post.get(key)).lower() != str(value).lower():
                    match = False
                    break

        if not match:
            continue

        # Check age range
        if min_age is not None or max_age is not None:
            try:
                age = int(post.get("age", -1))
                if min_age is not None and age < min_age:
                    continue
                if max_age is not None and age > max_age:
                    continue
            except ValueError:
                continue  # skip posts with non-integer or missing age

        # Check keyword inclusion
        text_lower = post['text'].lower()
        if include_keywords:
            if not any(kw.lower() in text_lower for kw in include_keywords):
                continue

        # Check keyword exclusion
        if exclude_keywords:
            if any(kw.lower() in text_lower for kw in exclude_keywords):
                continue

        filtered.append(post)

    return filtered

# Main function
def generate_wordcloud():
    stopwords = load_stopwords("stopwords.txt")
    posts = load_posts("posts.json")

    # EXAMPLE FILTERING
    include_keywords = ["python"]          # only include posts with this word that it will only recive words with that keyword in the sentence
    exclude_keywords = ["hate", "bad"]     # exclude posts with these words or more bad words depending or words that the owner doesn't want to see
    filters = {
        "gender": "female",                # only posts by females but can edit to male
        "region": "california"             # only from California can change where you want your data from
    }

    filtered = filter_posts(
        posts,
        include_keywords = include_keywords,
        exclude_keywords = exclude_keywords,
        filters = filters,
        min_age = 20
    )

    # It will combine the text together
    all_text = " ".join(post["text"] for post in filtered)

    # This will remove all the stop words
    words = [word for word in all_text.split() if word.lower() not in stopwords]

    cleaned_text = " ".join(words)

    # This will create the word cloud as a picture
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(cleaned_text)

    # This will display the image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("output.png")
    plt.show()

if __name__ == "__main__":
    generate_wordcloud()